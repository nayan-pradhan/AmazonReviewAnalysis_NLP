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

