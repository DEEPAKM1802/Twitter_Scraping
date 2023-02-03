# Twitter_Scraping
To run the following code:

1) Go to cmd in windows

2) type cd {file path where the script is saved}

3) type streamlit run twitter_scraping.py

*************************************************************************************************************************************************************************



The following is the first project from GUVI datascience course regarding twitter scraping, storing the result in mongodb and building a solid UI from user interaction.

The first block of code includes all the imports for packages used in the program.

The second block of code is a function for twiterscraping. The function requires two parameters:
    1. query : Should be based on twiter advance search function
    2. limit: How many data row user expects
The function returns the output in dataframe created using pandas.

The third function is for establishing connection with mongodb database and store all the data from the above function in tweet database in twiter collection.
The data is only uploaded if the user clicks upload button.

The third block of code is the actual UI where user can pass the input. streamlit poackage is used for the UI.
It includes textboxes headers, dataframe and upload and download button.

The last cell is just a main call to the UI from which entire code is excuted.
