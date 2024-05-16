# #Healthcare Evolving Adaptive Learning Intelligent Qualifier
# #Pronounced Heal IQ, might drop the IQ.
# import re
# import random
# import difflib
# # from nltk.corpus import wordnet
# # import nltk
# # import requests

# # Download WordNet data
# nltk.download('wordnet')

# # Function to get synonyms using NLTK WordNet
# def get_synonyms(word):
#     synonyms = []
#     for syn in wordnet.synsets(word):
#         for lemma in syn.lemmas():
#             synonyms.append(lemma.name())
#     return list(set(synonyms))

# # Synonyms dictionary. Not very important, but can still use it. 
# synonyms = {
#     'hurt': get_synonyms('hurt'),
#     'diagnosed': get_synonyms('diagnosed'),
#     'medications': get_synonyms('medications'),
#     'doctor': get_synonyms('doctor'),
#     'health concerns': get_synonyms('health concerns'),
#     'experience': get_synonyms('experience'),
#     'feeling': get_synonyms('feeling'),
#     'prescribed': get_synonyms('prescribed'),
#     'surgery': get_synonyms('surgery'),
#     'worried about': get_synonyms('worried about'),
#     'family history of': get_synonyms('family history of'),
#     'exercise routine': get_synonyms('exercise routine'),
# }

# # Eliza's patterns and responses
# patterns = [
#     (r'I experience (.+)', ['Tell me more about your experience with {0}.', 'How does {0} impact your daily life?']),
#     (r'I am feeling (.+)', ['Why do you think you are {0}?', 'How long have you been {0}?']),
#     (r'I was prescribed (.+)', ['How has the {0} been for you?', 'Have you noticed any changes since taking {0}?']),
#     (r'I am having surgery', ['Tell me more about the upcoming {0}. How do you feel about it?', 'What led to the decision for {0}?']),
#     (r'I am worried about (.+)', ['What concerns you about {0}?', 'How does {0} affect your emotions?']),
#     (r'Family history of (.+)', ['How does the family history of {0} impact your health?', 'Have you discussed this with your healthcare provider?']),
#     (r'Exercise routine', ['Can you describe your current {0}?', 'How do you stay active in your daily life?']),
#     (r'I have (.+)', ['Can you tell me more about your {0}?', 'How does your {0} affect you?']),
#     (r'I feel (.+)', ['Why do you feel {0}?', 'How long have you been feeling {0}?']),
#     (r'My (.+) hurts', ['Tell me more about the {0}.', 'When did you first notice the {0}?']),
#     (r'I am diagnosed with (.+)', ['How has the {0} affected your life?', 'What kind of treatment are you receiving for {0}?']),
#     (r'Medications', ['Can you tell me about any {0} you are taking?', 'Have you experienced any side effects from your {0}?']),
#     (r'Doctor', ['How often do you see your {0}?', 'What does your {0} say about your condition?']),
#     (r'Health concerns', ['Tell me more about any other {0} you have.', 'How are you managing your overall {0}?']),
# ]

# # Eliza's transformation function with synonym replacement
# def respond(message):
#     for pattern, responses in patterns:
#         match = re.search(pattern, message, re.IGNORECASE)
#         if match and match.group(1):
#             user_word = match.group(1).lower()
#             synonyms_list = synonyms.get(user_word, [user_word])
#             if synonyms_list:
#                 best_match = get_closest_match(user_word, synonyms_list)
#                 response = random.choice(responses)
#                 return response.format(best_match)

# def get_closest_match(word, synonyms_list):
#     if synonyms_list:
#         best_match = max(synonyms_list, key=lambda x: difflib.SequenceMatcher(None, word, x).ratio())
#         return best_match
#     else:
#         return word  # Return the original word if synonyms_list is empty

# # Conversation loop
# print("Hello, I'm HEAL-IQ. Type 'quit' to end the conversation.")
# while True:
#     user_input = input("You: ")
#     if user_input.lower() == 'quit':
#         break

#     eliza_response = respond(user_input)
#     print("HEAL-IQ:", eliza_response)