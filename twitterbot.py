import os
from urllib import response
import openai
import tweepy
import random
from requests.auth import HTTPBasicAuth
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Cannabis News API Key
cannabis_news_api_key = os.getenv("CANNABISNEWSAPIKEY")
cannabis_news_endpoint = os.getenv("CANNABIS_NEWS_ENDPOINT")

# Twitter API keys
twitter_consumer_key = os.getenv("TWITTER_CONSUMER_KEY")
twitter_consumer_secret = os.getenv("TWITTER_CONSUMER_SECRET")
twitter_access_token = os.getenv("TWITTER_ACCESS_TOKEN")
twitter_access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

# Initialize Twitter API client
auth = tweepy.OAuthHandler(twitter_consumer_key, twitter_consumer_secret)
auth.set_access_token(twitter_access_token, twitter_access_token_secret)
twitter_api = tweepy.API(auth)

# Function to fetch a news article from your database
def fetch_news_articles():
    params = {"limit": 1}
    headers = {'Accept': 'application/json'}
    auth = HTTPBasicAuth("apikey", cannabis_news_api_key)

    req = requests.get(cannabis_news_endpoint, params=params, headers=headers, auth=auth)
    response.raise_for_status() # Raise an exception for HTTP error

        
# Function to generate tweets using OpenAI

# Main function