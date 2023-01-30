#!/usr/bin/env python
# coding: utf-8

#**********************************************************************************************************************************************

#importing important packages
import snscrape.modules.twitter as sntwitter
import pandas as pd
import pymongo
import streamlit as st
import datetime
import os


#**********************************************************************************************************************************************


3 #function used for twiter scraping
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


#**********************************************************************************************************************************************


#function to upload data into mongo db (Please enter mongo url in conn)
def df_to_mongo(df, conn="****************************************************************************************"):
    client = pymongo.MongoClient(conn)
    db = client['tweets']
    collection = db['twiter']
    collection.insert_many(df.to_dict('records'))

    
#**********************************************************************************************************************************************


#streamlit function for UI
def streamlit_UI():

    #Title and header to be dispalyed
    colT1,colT2 = st.columns([1,3])
    with colT2:
        st.title(' :blue[Twitter Scraping]')
    header2 = st.subheader("Welcome!!! Please enter data to be searched")
 

    #Input field with submit button( form)
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
  

    #Displaying upload, and dowload buttons
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Upload"):
         df_to_mongo(df=data)
         st.success("Data uploaded successfully")
    with col2:
       st.download_button("Dowload CSV", data=data.to_csv(header=True, index=True), file_name="export_csv", on_click=None, disabled=False)
    with col3:
       st.download_button("Dowload json", data=data.to_json(), file_name="export_json", on_click=None, disabled=False)

    
    #Display output dataframe
    st.dataframe(data = data) 

    
#**********************************************************************************************************************************************


#Main call to UI which leads to excution of entire program
maincall = streamlit_UI()
