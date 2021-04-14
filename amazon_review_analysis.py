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

# def setup():
#     DRIVER_PATH= str(Path('chromedriver').resolve())
#     translator = google_translator()

def get_url():
    url_input = input("Enter Amazon URL: ")
    return(url_input)

# def get_trained_model():
#     # print("Importing Trained Model...", end="\r")
#     print("Starting...")
#     SVC_clf = pickle.load(open('saved_model.pickle', 'rb'))
#     print("                            ", end="\r") # clearing terminal space
#     # print("Imported Trained Model!", end="\r")

def start_scraping(user_input_URL):
    translator = google_translator()
    DRIVER_PATH= str(Path('chromedriver').resolve())
    driver = webdriver.Chrome(executable_path=DRIVER_PATH)
    driver.get(user_input_URL)
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')

    try:
        all_reviews_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="cr-pagination-footer-0"]/a')) # Find next page button
        )
        all_reviews_button.click()

        all_pages_reached = False
        comment_arr = []
        ratings_arr = []

        print("                               ", end="\r") # clearing terminal space
        pages = 0
        while pages < 15:
        # while not all_pages_reached:
            pages += 1
            print("Reading Page: {}".format(pages), end="\r")
            comments = soup.find_all('span', {'data-hook':'review-body'}) # Finding all reviews
            ratings = soup.find_all('i', {'data-hook':'review-star-rating'}) # Finding all ratings
            
            for comment in comments:
                comment_temp = comment.span.text
                time.sleep(0.2) # wait for page to load properly

                ## Translator gets blocked from Google's side if there are too many requests
                # if((translator.detect(comment_temp))[0]!='en'):
                #     comment_temp = translator.translate(comment_temp, lang_tgt='en')
                    
                comment_arr.append(comment_temp)
            
            for rating in ratings:
                rating_temp = float(rating.text[:3])
                ratings_arr.append(rating_temp)
            
            try:
                next_page_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="cm_cr-pagination_bar"]/ul/li[2]/a')) # Find next page button
                )
                next_page_button.click()
            except:
                print("Finished Reading Pages!", end="\r")
                all_pages_reached = True 
                break

        return comment_arr, ratings_arr, pages

    except:
        # print("Unexpeced Error Occured! Could not locate next page button. Are you sure your link is correct?", end="\r") 
        return [],[],0

# def predict_function(clf, string):
#     temp = clf.predict([string])
#     if (temp[0]==0):
#         return("Negative Review")
#     else:
#         return("Positive Review")


def start_predicting(comment_arr):
    clf = pickle.load(open('saved_model.pickle', 'rb'))

    # For Predicting
    pred_arr = []
    pos = 0
    neg = 0

    # Prediction
    for comment in comment_arr:
        comment_pred = clf.predict([comment])
        if comment_pred[0]==1:
            pos+=1
        else:
            neg+=1
        pred_arr.append(comment_pred)

    return pos, neg

def print_result(pos, neg, ratings_arr, pages):
    # Printing prediction and results
    print("Total number of pages scraped:", pages)
    print("Total number of reviews scraped:", pos+neg)
    print("Total number of positive reviews:", pos)
    print("Total number of negative reviews:", neg)
    # from scraping
    print("Average rating from reviewers:", '%.2f' % (sum(ratings_arr)/len(ratings_arr)))

def main():
    user_input_URL = get_url()
    # clf = get_trained_model()
    comment_arr, ratings_arr, pages = start_scraping(user_input_URL)
    if (len(comment_arr) > 0 and len(ratings_arr) > 0 and pages > 0):
        pos, neg = start_predicting(comment_arr)
        print_result(pos, neg, ratings_arr, pages)
        return 1
    else:
        print("Error: Please check your link and re-run the python file!")
        return 0

if __name__ == "__main__":
    main()