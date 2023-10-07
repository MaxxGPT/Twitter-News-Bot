from datetime import datetime
import logging

logger = logging.getLogger(__name__)

# Function to calculate the length of a tweet considering Twitter's specific rules
def calculate_tweet_length(tweet):
    url_count = tweet.count('http')
    return len(tweet) + (url_count * (23 - 6))  # Twitter counts URLs as 23 characters

# Function to post the generated tweet
def post_tweet(tweet_content, twitter_api):
    try:
        response = twitter_api.create_tweet(text=tweet_content)
        logger.info(f"{datetime.now()} - Tweet posted successfully: {tweet_content}")
    except Exception as e:
        logger.error(f"{datetime.now()} - An unexpected error occurred: {e}")
        logger.error(f"Exception type: {type(e)}")
