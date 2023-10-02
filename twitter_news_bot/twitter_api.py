from config import twitter_api
from datetime import datetime
from config import load_config
import tweepy

# Function to calculate the length of a tweet considering Twitter's specific rules
def calculate_tweet_length(tweet):
    url_count = tweet.count('http')
    return len(tweet) + (url_count * (23 - 6))  # Twitter counts URLs as 23 characters

# Function to post the generated tweet
def post_tweet(tweet_content):
    try:
        response = twitter_api.create_tweet(text=tweet_content)
        print(f"{datetime.now()} - Tweet posted successfully:", tweet_content)
    except Exception as e:  # Catch all exceptions
        print(f"{datetime.now()} - An unexpected error occurred: {e}")
        print(f"Exception type: {type(e)}")
