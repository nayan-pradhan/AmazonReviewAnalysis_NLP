import pandas as pd
from google_trans_new import google_translator
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pickle
from selenium import webdriver
from pathlib import Path 
from bs4 import BeautifulSoup
import train_model

def __init__(main):
    setup()
    get_url()
    get_trained_model()
    predict_function()
    start_scraping()
    start_predicting()
    print_result()