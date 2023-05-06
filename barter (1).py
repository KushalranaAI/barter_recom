# -*- coding: utf-8 -*-
"""Barter.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1rkIOGSIwglZcx__hT15NzFF_4o3Rf8-0
"""

## installing pymongo library to connect mongodb and python notebook
!pip install pymongo

!pip install dnspython

## importing mongoclient from pymongo to get access of data from database
from pymongo import MongoClient
import time
client = MongoClient(f"mongodb+srv://akshay_jangra:Adiyta12345@cluster0.wenn6ur.mongodb.net/?retryWrites=true&w=majority")
print(client.list_database_names())

# with client as cl:
#     db = cl.Barter
#     collection = db.users
#     for i in collection.find():
#         print(i)


db = client["Barter"]
collection = db["posts"]


# cursor = collection.find()
# for document in cursor:
#     print(document)
data = list(collection.find())

# print the first document in the list
print(data[0])

from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient(f"mongodb+srv://akshay_jangra:Adiyta12345@cluster0.wenn6ur.mongodb.net/?retryWrites=true&w=majority")
db = client["Barter"]
collection = db["posts"]

def get_data():
    # Retrieve data from MongoDB
    data = collection.find({})
    return data

import pandas as pd

data = get_data()

# convert the list of dictionaries to a Pandas DataFrame and set the index to "_id"
df = pd.DataFrame(data)

# set the index to "_id"
df = df.set_index("_id")


## selecting a important or required features 
data = df[['title','description','image','tags','tools','category']]

"""## Textual data pre-processing"""

## lower case all the data
# data['title'] = data['title'].str.lower()
data.loc[:, 'description'] = data['description'].str.lower()

def join_strings(strings, separator=', '):
    """
    Join a list of strings using a specified separator.
    
    Parameters:
        strings (list): A list of strings to join.
        separator (str): The separator to use between the strings.
    
    Returns:
        str: The joined string.
    """
    return separator.join(strings)

data['tags'] = data['tags'].apply(join_strings)
data['tools'] = data['tools'].apply(join_strings)
data['category'] = data['category'].apply(join_strings)

data['tags'] = data['tags'].str.lower()
data['tools'] = data['tools'].str.lower()

data['category'] = data['category'].str.lower()

data = data.drop(columns ='image', axis = 1)

## removing html tags
import re
def remove_html_tags(text):
  pattern = re.compile('<.*?>')
  return pattern.sub(r'', text)

# data['title'] = data['title'].apply(remove_html_tags)
data['description'] = data['description'].apply(remove_html_tags)
data['tags'] = data['tags'].apply(remove_html_tags)
data['tools'] = data['tools'].apply(remove_html_tags)
data['category'] = data['category'].apply(remove_html_tags)

## removing urls from data set
def remove_urls(text):
  patterns = re.compile(r'https?://\S+|www\.\S+')
  return patterns.sub(r'', text)

# data['title'] = data['title'].apply(remove_urls)
data['description'] = data['description'].apply(remove_urls)
data['tags'] = data['tags'].apply(remove_urls)
data['tools'] = data['tools'].apply(remove_urls)
data['category'] = data['category'].apply(remove_urls)

## performing punctuation on dataset
import string
exclude = string.punctuation

def remove_punct(text):
   return text.translate(str.maketrans('','', exclude))

# data['title'] = data['title'].apply(remove_punct)
data['description'] = data['description'].apply(remove_punct)
data['tags'] = data['tags'].apply(remove_punct)
data['tools'] = data['tools'].apply(remove_punct)
data['category'] = data['category'].apply(remove_punct)

import nltk

from nltk.corpus import stopwords
nltk.download('stopwords')

stop_words = set(stopwords.words('english'))

def remove_stopwords(text):
    words = text.split()
    clean_words = [word for word in words if word.lower() not in stop_words]
    return " ".join(clean_words)

# data['title'] = data['title'].apply(remove_stopwords)
data['description'] = data['description'].apply(remove_stopwords)
data['tags'] = data['tags'].apply(remove_stopwords)
data['tools'] = data['tools'].apply(remove_stopwords)
data['category'] = data['category'].apply(remove_stopwords)

## emoji removal
import re

def remove_emojis(text):
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002702-\U000027B0"  # other miscellaneous symbols
        u"\U000024C2-\U0001F251"  # enclosed characters
                           "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)

data['title'] = data['title'].apply(remove_emojis)
data['description'] = data['description'].apply(remove_emojis)
data['tags'] = data['tags'].apply(remove_emojis)
data['tools'] = data['tools'].apply(remove_emojis)
data['category'] = data['category'].apply(remove_emojis)

import spacy
nlp = spacy.load('en_core_web_sm')
def tokenize(text):
    # create a spacy document from the text
    doc = nlp(text)
    
    # extract the tokens from the document
    tokens = [token.text for token in doc]
    # Return tokens
    return tokens

# data['title'] = data['title'].apply(tokenize)
data['description'] = data['description'].apply(tokenize)
data['tags'] = data['tags'].apply(tokenize)
data['tools'] = data['tools'].apply(tokenize)
data['category'] = data['category'].apply(tokenize)

from nltk.stem import PorterStemmer

ps = PorterStemmer()

def stem_words(text):
    stemmed_words = []
    for word in text:
        stemmed_words.append(ps.stem(word))
    return " ".join(stemmed_words)


# data['title'] = data['title'].apply(stem_words)
data['description'] = data['description'].apply(stem_words)
data['tags'] = data['tags'].apply(stem_words)
data['tools'] = data['tools'].apply(stem_words)
data['category'] = data['category'].apply(stem_words)


from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# create a TfidfVectorizer object
tfidf = TfidfVectorizer(stop_words='english')

# create a TF-IDF matrix for the relevant features (description, tags, tools, category)
tfidf_matrix = tfidf.fit_transform(data['description'].astype(str) + ' ' + data['tags'].astype(str) + ' ' + data['tools'].astype(str) + ' ' + data['category'].astype(str))

# calculate the cosine similarity between all posts
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# define a function to get recommendations based on a post title
def get_recommendations(title, data, cosine_sim):
    # reset the index of the data DataFrame to a numeric index
    data = data.reset_index(drop=True)

    # get the index of the post that matches the title
    idx = data[data['title'] == title].index[0]

    # get the cosine similarity scores for all posts
    sim_scores = list(enumerate(cosine_sim[idx]))

    # sort the posts by similarity score
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # get the indices of the top 10 similar posts (excluding the query post itself)
    top_indices = [i[0] for i in sim_scores[1:11]]

    # return the titles of the top 10 similar posts
    return data.loc[top_indices, 'title']

# example usage
query_title = 'Spotify App UI Concept'
recommendations = get_recommendations(query_title, data, cosine_sim)
print(recommendations)

import pickle
# save the model to a pickle file
with open('recommendation_model.pkl', 'wb') as f:
    pickle.dump((tfidf, cosine_sim, data), f)