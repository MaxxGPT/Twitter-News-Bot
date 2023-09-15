import os
from urllib import response
import openai
import tweepy
import random
from requests.auth import HTTPBasicAuth
import requests
from dotenv import load_dotenv
import openai

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
twitter_bearer_token = os.getenv("TWITTER_BEARER_TOKEN")

# Initialize Twitter API client
twitter_api = tweepy.Client(twitter_bearer_token, twitter_consumer_key, twitter_consumer_secret, twitter_access_token, twitter_access_token_secret, wait_on_rate_limit=False)

# Function to fetch a news article from your database
def fetch_news_articles():
    params = {"limit": 1, "ORG": "Weedmaps"}
    headers = {'Accept': 'application/json', 'apikey': cannabis_news_api_key}
    
    try:
        response = requests.get(cannabis_news_endpoint, params=params, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP error

        # Check if the response status code is 200 (OK)
        if response.status_code == 200:
            # Parse the JSON response
            json_response = response.json()

            # Extract the first article from the articles list
            article = json_response['articles'][0]

            # Create a dictionary with the data you want to use
            article_data = {
                "title": article['title'],
                "url": article['url'],
                "description": article['description'],
                "author": article['author'],
                "publishedAt": article['publishedAt'],
                "content": article['content'],
                "image_url": article['urlToImage'],
                "topic": article['Topic'],
                "sentiment": article['sentiment'],
            }

            print("Fetched Articles:")
            print(article_data)
            
            # Return the article_data dictionary
            return article_data
        else:
            print("Failed to retrieve articles. Status Code:", response.status_code)
            return None
    except requests.exceptions.RequestException as e:
        print("Error fetching news articles:", e)
        return None



        
# Function to generate tweets using OpenAI

def generate_tweet(article_data):
    prompt = (f"You are a cannabis news reporter. Summarize the following news article in a casual tone "
              f"and provide a general commentary or prediction based on the title, URL, sentiment, and topic. "
              f"\n\nTitle: {article_data['title']}\nURL: {article_data['url']}\nSentiment: {article_data['sentiment']}\nTopic: {article_data['topic']}\n"
              f"\nGenerate a tweet mentioning that the article was retrieved from cannabisnewsapi.ai and includes the article's URL.")

    max_tweet_length = 280  # Maximum length of a tweet in characters

    # Loop until a tweet within the character limit is generated
    while True:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            temperature=0.7,
            max_tokens=50  # Limit the tweet to a reasonable number of tokens to avoid very long outputs
        )
        generated_tweet = response.choices[0].text.strip()

        # Check if the generated tweet is within the allowed character limit
        if len(generated_tweet) <= max_tweet_length:
            return generated_tweet

# Function to post a tweet to Twitter
def post_tweet(tweet_content):
    try:
        # Print the length of the tweet content
        print("Tweet Content Length:", len(tweet_content))
        
        # Post the tweet using Tweepy
        response = twitter_api.create_tweet(text=tweet_content)
        print("Tweet posted successfully:", tweet_content)
    except tweepy.errors.TweepyException as e:
        print("Error posting tweet:", e)


# Main function

def main():
    # Fetch a news article from your database
    article_data = fetch_news_articles()

    if article_data:
        # Generate a tweet based on the news article
        tweet = generate_tweet(article_data)

        # Print the generated tweet
        print("Generated Tweet:")
        print(tweet)

        # Post the generated tweet to Twitter
        post_tweet(tweet)


if __name__ == "__main__":
    main()