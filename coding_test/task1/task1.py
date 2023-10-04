# [Task 1 | Web Scraping] Please write a piece of code to scrape and summarize the userID, 
# userName, pinned Tweet ID, and creation date of your own account with Twitter Official API

import tweepy
import pandas as pd

# Twitter API keys and tokens constants from developer portal
API_KEY = 'MPrJQnhMiCyAU9owkfMcX6vfC'
API_KEY_SECRET = '4dmFqd8GD5vwm0BqehHaD9eRuKck6cZuU47rbAtG9XHCHxEfJ6'
ACCESS_TOKEN = '1708239068633387008-myTLcBtjK066fx9Mfx7UxYAyMLP4xP'
ACCESS_TOKEN_SECRET = "zpoIkPS1GpE2xTv6wp7XNk907sf7ZkPlTmYoWRUBDVp3g"

#using API v2
#initializing a Tweepy API client 
client = tweepy.Client(
    consumer_key=API_KEY,
    consumer_secret=API_KEY_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET)

#to get information about my account, this returns a Response object
user = client.get_me(expansions='pinned_tweet_id', user_fields=['created_at','id','username'])

#get info desired from the 'data' and 'includes' fields
user_id = user.data.id
username = user.data.username
pinned_tweet_id = user.includes['tweets'][0].id #print only the id for the pinned tweet
creation_date = user.data.created_at.strftime("%Y-%m-%d %H:%M:%S") #format datetime to string

#Create a dataframe to summarize data
acc_info = {
    'User ID': [user_id],
    'User Name': [username],
    'Pinned Tweet ID': [pinned_tweet_id],
    'Creation Date': [creation_date]
}
df = pd.DataFrame(acc_info)
# the csv file will be saved to current working directory
df.to_csv('twi_account_info.csv', index=False)
print(f'csv file exported')

print("User ID:", user.data.id)
print("User Name:", user.data.username)
print("Pinned Tweet ID:", user.includes['tweets'][0].id)
print("Creation Date:", user.data.created_at.strftime("%Y-%m-%d %H:%M:%S"))


##first attempt with API v1.1

# auth = tweepy.OAuthHandler(API_key, API_key_secret)
# auth.set_access_token(access_token, access_token_secret)
# api = tweepy.API(auth)
# user = api.verify_credentials()

# user_id = user.id
# user_name = user.screen_name
# #pinned_tweet_id = user.pinned_tweet_id
# creation_date = user.created_at.strftime("%Y-%m-%d %H:%M:%S")
# print("User ID:", user_id)
# print("User Name:", user_name)
# #print("Pinned Tweet ID:", pinned_tweet_id)
# print("Creation Date:", creation_date)