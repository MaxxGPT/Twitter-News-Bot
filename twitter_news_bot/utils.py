from datetime import datetime

def calculate_tweet_length(tweet):
    url_count = tweet.count('http')
    return len(tweet) + (url_count * (23 - 6))  # Twitter counts URLs as 23 characters

def log_message(message):
    print(f"{datetime.now()} - {message}")

# Any other utility functions that you may need
