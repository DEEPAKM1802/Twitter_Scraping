#!/usr/bin/env python
# coding: utf-8


# **********************************************************************************************************************************************
# importing important packages
import pandas as pd
import pymongo
import snscrape.modules.twitter as sntwitter
import streamlit as st
from datetime import datetime, timedelta
import time
import base64


# **********************************************************************************************************************************************


# function used for twiter scraping
def twiter_scraping(query, limit):
    tweets = []
    latest_iteration = st.empty()
    bar = st.progress(0)
    # Scrapping twiter based on the inputs
    for tweet in sntwitter.TwitterSearchScraper(query).get_items():
        if len(tweets) == limit:
            break
        else:
            tweets.append(
                [query, datetime.now(), tweet.date, tweet.id, tweet.url, tweet.content, tweet.username,
                 tweet.replyCount, tweet.retweetCount, tweet.lang, tweet.source, tweet.likeCount])

            for i in range(10):
                li = latest_iteration.text(
                    f"In progress : ({len(tweets)}/{limit})  {int((len(tweets) / limit) * 100)}%")
                pb = bar.progress(int((len(tweets) / limit) * 100))
                time.sleep(0.01)
    time.sleep(1)
    li.empty()
    pb.empty()

    # Storing the scrapped data into dataframe(i.e. df)
    df = pd.DataFrame(tweets,
                      columns=['Search Query', 'Timestamp', 'date', 'id', 'url', 'tweet content', 'user', 'reply count',
                               'retweet count', 'language', 'source', 'like count'])

    return df


# **********************************************************************************************************************************************


# function to upload data into mongo db (Please enter mongo url in conn)
def df_to_mongo(df,
                conn="mongodb://deepakmongo:!AMDEEPAK1802@ac-hmiqjuj-shard-00-00.vk1yvh9.mongodb.net:27017,ac-hmiqjuj-shard-00-01.vk1yvh9.mongodb.net:27017,ac-hmiqjuj-shard-00-02.vk1yvh9.mongodb.net:27017/?ssl=true&replicaSet=atlas-wzamdc-shard-0&authSource=admin&retryWrites=true&w=majority"):
    client = pymongo.MongoClient(conn)
    db = client['twitter']
    collection = db['tweets']
    collection.insert_many(df.to_dict('records'))


# **********************************************************************************************************************************************


# streamlit function for UI
def streamlit_UI():
    st.set_page_config(layout="wide")

    # Input field displayed in columns
    with st.sidebar:
        text = st.text_input('Text', placeholder="Enter Text", disabled=False, label_visibility="visible")
        user = st.text_input('User', placeholder="Enter Username", disabled=False, label_visibility="visible")
        hata = st.text_input('#Hastags', placeholder="Enter Hastags", disabled=False, label_visibility="visible")
        stdate = st.date_input("From Date", value=(datetime.now() - timedelta(days=1)), disabled=False,
                               label_visibility="visible")
        eddate = st.date_input("To Date", disabled=False, label_visibility="visible")
        limit = st.number_input("No. of records", min_value=int(1), max_value=int(9999), value=int(1), step=int(1),
                                disabled=False, label_visibility="visible")

    # Title and header to be dispalyed
    colT1, colT2 = st.columns([3, 5])
    with colT2:
        st.title(' :blue[Twitter Scraping]')

    # Concatenate the input to be searched
    query = f"{text} until:{eddate} since:{stdate}"
    if hata != "":
        query = f"{text} (#{hata}) until:{eddate} since:{stdate}"
    if user != "":
        query = f"{text} (#{hata}) (from:{user}) until:{eddate} since:{stdate}"
    limit = int(limit)

    try:
        data = None
        # Calling twiter function to scrape data based on the user input
        if text != "" or hata != "" or user != "":
            data = twiter_scraping(query, limit)

        # Displaying upload, and dowload buttons
        if data.empty == False:
            col1, col2, col3 = st.columns([6, 1, 0.9])
            with col1:
                up_btn = st.button("Upload", help="Click to Upload the data in MongoDB")
            if up_btn:
                df_to_mongo(df=data)
                st.success("Data uploaded successfully", icon="✅")
            with col2:
                st.download_button("Dowload CSV", data=data.to_csv(header=True, index=True), file_name="export_csv",
                                   on_click=None, disabled=False)
            with col3:
                st.download_button("Dowload json", data=data.to_json(), file_name="export_json", on_click=None,
                                   disabled=False)

            # Display output dataframe
            st.dataframe(data=data)
        else:
            st.info("No Records Found")
    except:
        if text == "" or hata == "" or user == "":
            st.info("Please Enter Data In The Sidemenu")
            file_ = open("C:\\Users\\ADMIN\\Downloads\\VHXm.gif", "rb")
            contents = file_.read()
            data_url = base64.b64encode(contents).decode("utf-8")
            file_.close()

            st.markdown(
                f'<img src="data:image/gif;base64,{data_url}" alt="cat gif" width="1000" height="400">',
                unsafe_allow_html=True,
            )
        else:
            st.warning("""Opps! Something went wrong\n
                       Try the following:\n
                        1. Enter lower value in 'No. of records'.\n
                        2. Please check the data entered is correctly spelled.""")


# **********************************************************************************************************************************************


# Main call to UI which leads to excution of entire program
maincall = streamlit_UI()
