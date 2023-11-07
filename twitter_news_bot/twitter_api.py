from datetime import datetime
import logging
import tweepy
import os
import json

logger = logging.getLogger(__name__)

def initialize_twitter_api():
    twitter_consumer_key = os.environ.get("TWITTER_CONSUMER_KEY")
    twitter_consumer_secret = os.environ.get("TWITTER_CONSUMER_SECRET")
    twitter_access_token = os.environ.get("TWITTER_ACCESS_TOKEN")
    twitter_access_token_secret = os.environ.get("TWITTER_ACCESS_TOKEN_SECRET")
    twitter_bearer_token = os.environ.get("TWITTER_BEARER_TOKEN")

    if not all([twitter_consumer_key, twitter_consumer_secret, twitter_access_token, twitter_access_token_secret, twitter_bearer_token]):
        raise Exception("Twitter environment variables are not set correctly.")

    return tweepy.Client(twitter_bearer_token, twitter_consumer_key, twitter_consumer_secret, twitter_access_token, twitter_access_token_secret, wait_on_rate_limit=True)

def lambda_handler(event, context):
    # The event is expected to contain the tweet content under the 'tweet_content' key
    tweet_content = event.get('tweet_content')

    if not tweet_content:
        logger.error(f"No tweet content to post at {datetime.now()}")
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'No tweet content provided'})
        }
    
    try:
        twitter_api = initialize_twitter_api()
        post_tweet(tweet_content, twitter_api)
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Tweet posted successfully'})
        }
    except Exception as e:
        logger.error(f"Failed to post tweet at {datetime.now()}: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Internal server error'})
        }

# Function to calculate the length of a tweet considering Twitter's specific rules
def calculate_tweet_length(tweet):
    url_count = tweet.count('http')
    return len(tweet) + (url_count * (23 - 6))  # Twitter counts URLs as 23 characters

# Function to post the generated tweet
def post_tweet(tweet_content, twitter_api):
    try:
        response = twitter_api.create_tweet(text=tweet_content)
        logger.info(f"{datetime.now()} - Tweet posted successfully: {tweet_content}")
        return response
    except Exception as e:
        logger.error(f"{datetime.now()} - An unexpected error occurred: {e}")
        logger.error(f"Exception type: {type(e)}")
        raise
