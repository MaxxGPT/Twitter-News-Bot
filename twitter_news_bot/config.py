import os
from dotenv import load_dotenv
import tweepy

# Load environment variables from .env file
load_dotenv()

def initialize_twitter_api():
    twitter_consumer_key = os.getenv("TWITTER_CONSUMER_KEY")
    twitter_consumer_secret = os.getenv("TWITTER_CONSUMER_SECRET")
    twitter_access_token = os.getenv("TWITTER_ACCESS_TOKEN")
    twitter_access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

    if not all([twitter_consumer_key, twitter_consumer_secret, twitter_access_token, twitter_access_token_secret]):
        raise Exception("Twitter environment variables are not set correctly.")

    auth = tweepy.OAuthHandler(twitter_consumer_key, twitter_consumer_secret)
    auth.set_access_token(twitter_access_token, twitter_access_token_secret)

    return tweepy.API(auth, wait_on_rate_limit=True)

def load_config():
    return {
        'OPENAI_API_KEY': os.getenv("OPENAI_API_KEY"),
        'cannabis_news_api_key': os.getenv("CANNABISNEWSAPIKEY"),
        'CANNABIS_NEWS_ENDPOINT': os.getenv("CANNABIS_NEWS_ENDPOINT"),
        'max_retries': 5,
        'max_total_attempts': 50
    }
