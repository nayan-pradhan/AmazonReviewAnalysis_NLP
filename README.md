# Amazon Review Analysis using ML, NLP, and Web Scraping

## Introduction
This project uses Machine Learning, Natural Language Processing (NLP), and Web Scraping in order to get real customer reviews for any product on Amazon (only [amazon.com](https://www.amazon.com) supported for now) and perform sentiment analysis that predicts whether the reviews are positive or negative.

## Setup and Deployment
1. Clone the repository into your local machine: 
```bash
git clone https://github.com/nayan-pradhan/AmazonReviewsAnalysis_NLP
```
4. Navigate into your cloned local directory and setup a virtual environment: 
```bash
pip3 install virtualenv
virtualenv venv
source venv/bin/activate
```
3. Install all requirement libraries: 
```bash
pip3 install -r requirements.txt
```
4. Run the python file:
```bash
python3 amazon_review_analysis.py
```

## Files
1. **amazon_data.txt**: Training data.
2. **amazon_review_analysis.py**: Main script that gets the url, scrapes data from the amazon website, and predicts the sentiment.
3. **chromedriver**: Chrome driver to open url.
4. **requirements.txt**: All libraries/frameworks used.
5. **saved_model.pickle**: Trained model that gets saved automatically.
6. **script.ipynb**: Jupyter Notebook script that was used in order to test functions.
7. **train_model.py**: Script that trains the training data and builds the training model. This scipt is automatically executed when `amazon_review_analysis.py` is executed.
