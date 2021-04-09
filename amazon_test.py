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

## bug: WHEN PAGE HAS NO NEXT ELEMENT

DRIVER_PATH= str(Path('chromedriver').resolve())

user_input_URL = input("Enter Amazon URL: ")

# https://www.amazon.com/Acer-SB220Q-Ultra-Thin-Frame-Monitor/dp/B07CVL2D2S/ref=lp_16225007011_1_10?th=1

print("Importing Trained Model...", end="\r")
SVC_clf = pickle.load(open('saved_model.pickle', 'rb'))
print("Imported Trained Model!", end="\r")

translator = google_translator()
driver = webdriver.Chrome(executable_path=DRIVER_PATH)
driver.get(user_input_URL)
html = driver.page_source
soup = BeautifulSoup(html, 'lxml')

all_reviews_button = driver.find_elements_by_xpath('//*[@id="cr-pagination-footer-0"]/a')[0]
all_reviews_button.click()

all_pages_reached = False

comment_arr = []
ratings_arr = []

def predict_func(string):
    temp = SVC_clf.predict([string])
    if (temp[0]==0):
        return("Negative Review")
    else:
        return("Positive Review")

print("                               ", end="\r")  # clearing terminal space
pages = 0
while pages < 15:
# while not all_pages_reached:
    pages += 1
    print("Reading Page: {}".format(pages), end="\r")
    comments = soup.find_all('span', {'data-hook':'review-body'})
    ratings = soup.find_all('i', {'data-hook':'review-star-rating'})
    
    for comment in comments:
        comment_temp = comment.span.text
        time.sleep(0.2)
        
##         Translator gets blocked from Google's side if there are too many requests
#         if((translator.detect(comment_temp))[0]!='en'):
#             comment_temp = translator.translate(comment_temp, lang_tgt='en')
            
        comment_arr.append(comment_temp)
    
    for rating in ratings:
        rating_temp = float(rating.text[:3])
        ratings_arr.append(rating_temp)
    
    try:
        next_page_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="cm_cr-pagination_bar"]/ul/li[2]/a'))
        )
        next_page_button.click()
    except:
        print("Finished Reading Pages!", end="\r")
        all_pages_reached = True 
        break

pred_arr = []
pos = 0
neg = 0

for comment in comment_arr:
    comment_pred = predict_func(comment)
    if comment_pred=='Positive Review':
        pos+=1
    else:
        neg+=1
    pred_arr.append(comment_pred)
    
# print(pred_arr)
print("Total number of reviews scraped:", pos+neg)
print("Total number of positive reviews:", pos)
print("Total number of negative reviews:", neg)

# from scraping
print("Average rating from reviewers:", '%.2f' % (sum(ratings_arr)/len(ratings_arr)))