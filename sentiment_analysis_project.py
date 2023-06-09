# -*- coding: utf-8 -*-
"""Sentiment_Analysis_Project.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1dP2QcT6gONFjLH5VBCu3_uesMcfBePnw

## <center> NLP Sentiment Analysis for Customer Feedback

## 1.Problem Statement -

**This is an add-on project for a client that wants to learn about their customers' sentiments through feedback and ratings in order to retain them and enhance their services to fulfil their needs.

## 2.Importing Library for data gathering and EDA
"""

import pandas as pd 
import numpy as np
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import matplotlib.pyplot as plt
import seaborn as sns

import warnings
warnings.filterwarnings("ignore")

"""#### Collecting Data"""

nlp_raw_data = pd.read_csv('/content/data_sentiment_headphone.csv')
nlp_raw_data.head()

nlp_raw_data.tail()

nlp_raw_data.info()

nlp_raw_data.isna().sum()

nlp_raw_data.shape

sns.countplot(data=nlp_raw_data, x="rating")

nlp_raw_data.rating.value_counts()

"""#### Splitting of data"""

from sklearn.model_selection import train_test_split
X_train,X_test,y_train,y_test = train_test_split(nlp_raw_data.review,nlp_raw_data.rating,test_size=0.2,random_state=42)

X_train.head()

y_train.head()

"""#### Tokenization"""

# tokenization
def tokenization(data):
    tokens = word_tokenize(data)
    return tokens

import nltk
nltk.download("all")

x_train_token = X_train.apply(tokenization)
x_test_token =X_test.apply(tokenization)

x_train_token.head()

x_test_token.head()

"""#### Remove Punctuation"""

def remove_punctuation(data):
    clean_text = [x for x in data if x.isalpha()]
    return clean_text

x_train_without_punt = x_train_token.apply(remove_punctuation)
x_test_without_punt = x_test_token.apply(remove_punctuation)

x_train_without_punt.head()

"""#### Normalization"""

def normalization(data):
    lower = [x.lower() for x in data]
    return lower

x_train_normal = x_train_without_punt.apply(normalization)
x_test_normal = x_test_without_punt.apply(normalization)

x_train_normal.head()

"""#### Stopwaords Removal"""

domain_stop_w = ["headphone", 'delivery', 'delivered','product','voice']
def stopwords_remove(data):
    from nltk.corpus import stopwords
    stop = stopwords.words('english')
    clean_text = [x for x in data if x not in stop and x not in domain_stop_w]
    return clean_text

x_train1= x_train_normal.apply(stopwords_remove)
x_test1= x_test_normal.apply(stopwords_remove)

x_train1.head()

x_test1.head()

"""#### Lemitazation"""

def lemmatization(data):
    from nltk.stem import WordNetLemmatizer
    lemma = WordNetLemmatizer()
    l1 = []
    for i in data :
        text1 = lemma.lemmatize(i)
        l1.append(text1)
    return l1

final_train = x_train1.apply(lemmatization)
final_test = x_test1.apply(lemmatization)

final_train.head()

final_test.head()

"""### World Cloud"""

from wordcloud import WordCloud,STOPWORDS
stopwords = set(STOPWORDS)
def show_wordcloud(data):
    wordcloud= WordCloud(background_color='white',stopwords=stopwords,max_words=100,max_font_size=30,scale=3,random_state=1)
    wordcloud = wordcloud.generate(str(data))
    fig = plt.figure(1,figsize=(15,15))
    plt.axis('off')
    plt.imshow(wordcloud)
    plt.show()
    
show_wordcloud(final_test)

"""#### Joining Words"""

def join_list(data):
    text = " ".join(data)
    return text

final_text_train = final_train.apply(join_list)
final_text_test = final_test.apply(join_list)

final_text_train

final_text_test

"""## 1. CountVectorizer"""

from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(lowercase=True,stop_words='english',max_df=0.95,max_features=1200)
count_train = cv.fit_transform(final_text_train)
count_test = cv.transform(final_text_test)

"""#### final DF for analysis"""

df = pd.DataFrame(count_train.A)

df.head()

df.shape

"""## Model Building

#### Naive Bayes - MultinomialNB
"""

from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
from sklearn.metrics import ConfusionMatrixDisplay
from sklearn.metrics import classification_report

mnb_model = MultinomialNB()
mnb_model.fit(count_train.A,y_train)
pred_mnb = mnb_model.predict(count_test.A)

pred_mnb

report = classification_report(y_test,pred_mnb)
print(report)