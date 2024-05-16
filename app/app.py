from flask import Flask, render_template, request, session
from database import get_database_connection
import random
from collections import Counter
import openai
import re
import config

app = Flask(__name__)

exclude_symptoms = set()
last_asked_symptom = ""

# Initialize database connection
mydb = get_database_connection()

# Set your OpenAI API key
openai.api_key = 'Your Key Here'
model = "gpt-3.5-turbo-instruct"

# # Health-related patterns and responses for Eliza
patterns = [
    (r'yes', ['Thank you.']),
    (r'no', ['What you do not have is not as important. Lets focus on symptoms you do have.']),
    (r'(.+)', ['{0}? Thank you'])
]


def gptResponses(user_input):
    global textResponse
    response = openai.Completion.create(
        engine=model,
        prompt='''You are a friendly health chatbot.If the user seems to get off track and does not mention any symptom 
        of a disease in their message, then guide them appropriately to enter the symptoms they are 
        experiencing. Keep your responses short though and to the point. Do not ask the user any questions.
        ''' + user_input,
        max_tokens=100
    )
    # test this a little more, its looping and showing multiple texts
    for choice in response.choices:
        # Store the text 
        textResponse = choice.text.strip()
        print("Text Response", textResponse)
    return textResponse


def respond(message):
    for pattern, responses in patterns:
        match = re.search(pattern, message, re.IGNORECASE)
        if match:
            user_word = match.group(1).lower() if match.groups() else match.group(0).lower()
            response = random.choice(responses)
            return response.format(user_word)
    # Default response, will never reach
    return "I'm sorry, I didn't quite understand that. Could you please provide more details?"


total = ""


def clear_list():
    global total
    total = ""


# Define a function to process user inputs
def process_input(user_input, specific_words):
    # Check if user input contains any of the specific words or phrases
    if specific_words != "":
        for word in specific_words.split(','):
            if word.strip().lower() in user_input.lower():
                return f"True_{word.strip()}"

    # Check if user input is agreeing or disagreeing
    if re.search(r'\b(yes|yeah|sure|ok|okay|alright|right|agreed)\b', user_input, re.IGNORECASE):
        return "True_yes"
    elif re.search(r'\b(no|nah|nope|not really|disagree)\b', user_input, re.IGNORECASE):
        return "True_no"

    # Check if user input indicates they are finished
    finished_phrases = ["i am done", "i have no more symptoms", "give me my results", "i am finished", "done", "finish",
                        "finished", "stop", "results"]
    if any(phrase in user_input.lower() for phrase in finished_phrases):
        return "False_finished"

    text_response = gptResponses(user_input)

    return text_response


def clean_symptoms_list(sympt):
    # Convert each tuple in filtered_sorted_symptoms to a string
    s_words = [' '.join(map(str, symptom)) for symptom in sympt]

    # Remove everything except words, spaces, and commas from each string
    s_words = [re.sub(r'[^a-zA-Z\s,]', '', word) for word in s_words]

    # Convert the list of strings into a single string
    s = ' '.join(s_words)

    # Define the characters to be removed
    remove_chars = "'0123456789"

    # Create a translation table that maps every character from remove_chars to None
    table = str.maketrans('', '', remove_chars)

    # Use the translation table to remove the characters from the string
    s_words_str = s.translate(table)

    s_words_str = s_words_str.replace("   ", ",")
    s_words_str = s_words_str.replace("  ", ",")
    return s_words_str


# Route to render the HTML page with conversation history and input form
@app.route('/', methods=['GET', 'POST'])
def index():
    eliza_response = "Hi"
    global last_asked_symptom
    # Clear session if it's a GET request (page reload)
    if request.method == 'GET':
        session.pop('conversation', None)  # Clear conversation from session
        clear_list()

    conversation = session.get('conversation', [])

    if request.method == 'POST':
        user_input = request.form['user_input']

        print("user input: ", user_input)

        # Search DB and pull all the diseases with symptoms that are present in user_input
        cursor = mydb.cursor(dictionary=True)
        # Split user_input into words
        user_input_words = user_input.split()
        query = "SELECT * FROM disease_symptoms WHERE "  # Construct the SQL query dynamically
        # Create a placeholder for each word
        placeholders = ["symptoms LIKE %s" for _ in user_input_words]
        query += " OR ".join(placeholders)
        # Execute the query with each word in user_input_words
        cursor.execute(query, ['%' + word + '%' for word in user_input_words])
        results = cursor.fetchall()

        # Extract symptoms from the results
        symptoms_from_results = user_input_words

        # Extract symptoms from the results and split them into individual symptoms
        all_symptoms = [symptom for row in results for symptom in row['symptoms'].split(',')]

        # Count the frequency of each symptom
        symptom_counts = Counter(all_symptoms)

        # Sort symptoms by frequency in decreasing order
        sorted_symptoms = sorted(symptom_counts.items(), key=lambda x: x[1], reverse=True)

        # clean up sorted symptoms so symptoms can be split
        specific_words_str = clean_symptoms_list(sorted_symptoms)

        useful_input = process_input(user_input, specific_words_str)

        print("Matching symptom: ", useful_input)

        split_index = useful_input.find('_')  # find the index of the first underscore
        first_string = useful_input[:split_index]  # get the substring before the first underscore
        second_string = useful_input[split_index + 1:]  # get the substring after the first underscore

        print("First string:", first_string)
        print("Second string:", second_string)

        if first_string.__contains__("True"):
            if second_string.__contains__("yes"):
                exclude_symptoms.add(last_asked_symptom)
            elif second_string.__contains__("no"):
                print("they said no")
            else:
                exclude_symptoms.add(second_string)

        print("Excluded Symptoms", exclude_symptoms)

        # Normalize symptoms from the initial user input and the results
        normalized_exclude_symptoms = set(symptom.strip().lower() for symptom in exclude_symptoms)

        # Filter out excluded symptoms from sorted_symptoms
        filtered_sorted_symptoms = [(symptom, count) for symptom, count in sorted_symptoms if
                                    symptom.strip().lower() not in normalized_exclude_symptoms]

        if filtered_sorted_symptoms and filtered_sorted_symptoms[0][0]:
            last_asked_symptom = filtered_sorted_symptoms[0][0]

        if second_string.__contains__("finished"):
            filtered_sorted_symptoms = ""

        # Now, filtered_sorted_symptoms contains symptoms in decreasing order of frequency, excluding the ones found
        # in the first query
        if filtered_sorted_symptoms:
            highest_frequency_symptom = filtered_sorted_symptoms[0][0]
            if first_string.__contains__("True"):
                eliza_response = respond(second_string) + " Lets continue to narrow down. Do you have " + str(
                    highest_frequency_symptom) + "?" + " Your current symptom list is: " + ', '.join(exclude_symptoms)
            else:
                eliza_response = second_string

            # Now we need to handle the user responses in a way that we also understand the context of the Yes and
            # No. We will still need some text cleaning on this and still be able to retrieve the symptoms
        elif first_string.__contains__("False"):
            # Split excluded_symptoms into words
            excluded_symptoms_words = list(exclude_symptoms)

            # Remove leading/trailing spaces and convert to lower case
            excluded_symptoms_words = [word.strip().lower() for word in excluded_symptoms_words]

            print("final symptoms: ", excluded_symptoms_words)

            # Construct the SQL query dynamically
            query = """
            SELECT disease, frequency, symptom_count, symptom_count * frequency as score
            FROM (
                SELECT disease, frequency,
                """
            query += "SUM("
            for word in excluded_symptoms_words:
                query += f"CASE WHEN symptoms LIKE '%{word}%' THEN 1 ELSE 0 END + "

            # Remove the last '+' sign
            query = query[:-2]
            query += ") as symptom_count "

            query += """
                FROM disease_symptoms
                GROUP BY disease, frequency
                HAVING symptom_count > 0
            ) as subquery
            ORDER BY score DESC
            """

            cursor.execute(query)

            # Fetch all the results
            results = cursor.fetchall()

            print("query: ", query)
            print("results: ", results)

            # Convert the results to a string
            # Convert the results to a string
            result_string = '\n'.join([
                f"{result['disease']} (Symptom Count: {result['symptom_count']}, Frequency: {result['frequency']}, "
                f"Score: {result['score']}) "
                for result in results])
            split_string = result_string.split("\n")
            first_10 = split_string[:10]
            top_10 = "\n".join(first_10)

            print("results string", result_string)
            print("Top 10: ", top_10)

            eliza_response = "okay ill review what you told me to determine possible diseases, ailments, " \
                             "or disorders. The list hat matches your symptoms is: " + top_10

        else:
            print("No additional symptoms found.")

        # eliza_response = respond(user_input)
        conversation.append({'user_input': user_input, 'eliza_response': eliza_response})
        session['conversation'] = conversation  # Update conversation in session
        return render_template('index.html', conversation=conversation)

    return render_template('index.html', conversation=conversation)


if __name__ == '__main__':
    # Configure the Flask app
    app.config['SECRET_KEY'] = config.SECRET_KEY
    app.config['SESSION_TYPE'] = config.SESSION_TYPE
    app.run(debug=True)
