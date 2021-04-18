import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
import string
from spacy.lang.en.stop_words import STOP_WORDS
import spacy
from sklearn.svm import LinearSVC
import pickle 

## Reading training data
data = pd.read_csv('amazon_data.txt', sep='\t', header=None)
data.columns = ["Review", "Sentiment"]

## Helpers for cleaning
punctuation = string.punctuation
stop_words = list(STOP_WORDS)
nlp = spacy.load("en_core_web_sm")
numbers = string.digits

## Function that cleans input text
def cleaning_function(input_text):
    text = nlp(input_text)
    tokens = []
    for token in text:
        temp = token.lemma_.lower()
        tokens.append(temp)
    cleaned_tokens = []
    for token in tokens:
        if token not in stop_words and token not in punctuation and token not in numbers:
            cleaned_tokens.append(token)
    return cleaned_tokens

## X, y labels
X = data["Review"]
y = data["Sentiment"]

## SVC using tfidf (bag of words)
tfidf = TfidfVectorizer(tokenizer = cleaning_function)
classifier = LinearSVC()
SVC_clf = Pipeline([('tfidf', tfidf), ('clf', classifier)])
SVC_clf.fit(X, y)

## Saving trained model
fname = 'saved_model.pickle'
with open(fname, 'wb') as f:
    pickle.dump(SVC_clf, f)