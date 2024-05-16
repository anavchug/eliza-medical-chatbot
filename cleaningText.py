import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

def filter_medical_tokens(text):
    # Preprocessing
    text = re.sub('[^a-zA-Z]', ' ', text.lower())

    # Tokenization
    tokens = nltk.word_tokenize(text)

    # Part-of-speech tagging
    pos_tags = nltk.pos_tag(tokens)

    # Lemmatization and filtering
    lemmatizer = WordNetLemmatizer()
    filtered_tokens = []
    for word, tag in pos_tags:
        if tag.startswith('N') or tag.startswith('J'):  # Noun or Adjective
            word = lemmatizer.lemmatize(word)
            if word not in stopwords.words('english'):
                filtered_tokens.append(word)
    
    return filtered_tokens

# Example usage
new_review = 'I experience Fatigue and Fever'
filtered_tokens = filter_medical_tokens(new_review)
print(filtered_tokens)
