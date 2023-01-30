#!/usr/bin/env python
# coding: utf-8

# In[2]:


import snscrape.modules.twitter as sntwitter
import pandas as pd
import pymongo
import streamlit as st
import datetime
import os


# In[12]:


def twiter_scraping(query, limit):
    
    tweets = []
    #Scrapping twiter based on the inputs
    for tweet in sntwitter.TwitterSearchScraper(query).get_items():  
        if len(tweets) == limit:
            break
        else:
            tweets.append([query, datetime.datetime.now(), tweet.date, tweet.id, tweet.url, tweet.content,  tweet.username, tweet.replyCount, tweet.retweetCount, tweet.lang, tweet.source, tweet.likeCount])   

    #Storing the scrapped data into dataframe(i.e. df)       
    df = pd.DataFrame(tweets, columns=['Search Query', 'Timestamp', 'date', 'id', 'url', 'tweet content', 'user', 'reply count', 'retweet count', 'language', 'source', 'like count'])
    
    return df


# In[13]:


def df_to_mongo(df, conn="mongodb://deepakmongo:!AMDEEPAK1802@ac-hmiqjuj-shard-00-00.vk1yvh9.mongodb.net:27017,ac-hmiqjuj-shard-00-01.vk1yvh9.mongodb.net:27017,ac-hmiqjuj-shard-00-02.vk1yvh9.mongodb.net:27017/?ssl=true&replicaSet=atlas-wzamdc-shard-0&authSource=admin&retryWrites=true&w=majority"):
    client = pymongo.MongoClient(conn)
    db = client['tweets']
    collection = db['twiter']
    collection.insert_many(df.to_dict('records'))


# In[ ]:


def streamlit_UI():

    #Input fields to be dispalyed
    colT1,colT2 = st.columns([1,3])
    with colT2:
        st.title(' :blue[Twitter Scraping]')
    header2 = st.subheader("Welcome!!! Please enter data to be searched")
    
    
    with st.form("my_form"):
         col1, col2, col3 = st.columns(3)

         with col1:
             text = st.text_input('Text', placeholder="Enter Text", disabled=False, label_visibility="visible")
             stdate = st.date_input("From Date", disabled=False, label_visibility="visible")
       

         with col2:
              hata = st.text_input('#Hastags', placeholder="Enter Hastags", disabled=False, label_visibility="visible")
              eddate = st.date_input("To Date", disabled=False, label_visibility="visible")
       

         with col3:
               user = st.text_input('User', placeholder="Enter Username", disabled=False, label_visibility="visible")
               limit = st.number_input("No. of records", disabled=False, label_visibility="visible")
         submitted = st.form_submit_button("Submit")
    
    #Concatenate the input to be searched
    query = f"{text} until:{eddate} since:{stdate}"
    if hata != "":
        query = f"{text} (#{hata}) until:{eddate} since:{stdate}"
    if user != "":
       query = f"{text} (#{hata}) (from:{user}) until:{eddate} since:{stdate}"   
    
    limit = int(limit)

    #Calling twiter function to scrape data based on the user input
    data = twiter_scraping(query, limit)
    
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("Upload"):
         df_to_mongo(df=data)
         st.success("Data uploaded successfully")
            
       

    with col2:
       st.download_button("Dowload CSV", data=data.to_csv(header=True, index=True), file_name="export_csv", on_click=None, disabled=False)
       

    with col3:
       st.download_button("Dowload json", data=data.to_json(), file_name="export_json", on_click=None, disabled=False)

    #Display output and buttons
    st.dataframe(data = data) 


# In[ ]:


maincall = streamlit_UI()
