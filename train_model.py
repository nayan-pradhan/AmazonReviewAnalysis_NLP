import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import string
from spacy.lang.en.stop_words import STOP_WORDS
import spacy
from sklearn.svm import LinearSVC
import time
import pickle 
import os

data = pd.read_csv('amazon_data.txt', sep='\t', header=None)
data.columns = ["Review", "Sentiment"]

punctuation = string.punctuation
stop_words = list(STOP_WORDS)
nlp = spacy.load("en_core_web_sm")
numbers = string.digits

## function that cleans input text
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

X = data["Review"]
y = data["Sentiment"]

## SVC using tfidf (bag of words)
tfidf = TfidfVectorizer(tokenizer = cleaning_function)
classifier = LinearSVC()
SVC_clf = Pipeline([('tfidf', tfidf), ('clf', classifier)])
# print("Training Model...", end="\r")
SVC_clf.fit(X, y)
# print("Model Trained!", end="\r")

fname = 'saved_model.pickle'
# os.mkfifo(fname)
print("Saving Model...", end="\r")
with open(fname, 'wb') as f:
    pickle.dump(SVC_clf, f)
    
print("Model Saved", end="\r")