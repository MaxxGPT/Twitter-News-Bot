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
            articles = response.json()

            # Print the entire articles list to inspect its structure
            print("Fetched Articles:")
            print(articles)
        else:
            print("Failed to retrieve articles. Status Code:", response.status_code)
    
    except requests.exceptions.RequestException as e:
        print("Error fetching news articles:", e)

        
# Function to generate tweets using OpenAI

def generate_tweet(news_summary):
    prompt = f"You are an expert on cannabis twitter bot that tweets news articles about cannabis. The data you have access to is a database of over 950k news articles. The fields of each articles are the following: _id, title, url, description, author, publishedAt, content, source_id, urlToImage, GPE, ORG, PERSON, Tokens, Topic, Topic_Contribution, sentiment, and sentiment_score. Using the previous mentioned, create a Twitter Tweet that summarizes the articles, gives a prediction or general commentary. Include the article’s url, mention the article’s sentiment, and Topic. Use a casual tone of a knowledgable cannabis news reporter. Make it a detailed and well thought out tweet. Mention that the articles was retrieved from cannabisnewsapi.ai Constraints: Do not include pretext or context in your response, only return the tweet. Maximum 10,000 characters and use bold and italic text formatting where appropriate.\n\n{news_summary}"
    
    max_tweet_length = 280  # Maximum length of a tweet
    
    # Loop until a tweet within the character limit is generated
    while True:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            temperature=0.7,
            max_tokens=max_tweet_length  # Limit the tweet to max_tweet_length tokens
        )
        generated_tweet = response.choices[0].text.strip()

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
    fetch_news_articles()

    # Generate a tweet based on the news article
    news_summary = "Here is a summary of the news article you fetched."
    tweet = generate_tweet(news_summary)

    # Print the generated tweet
    print("Generated Tweet:")
    print(tweet)

    # Post the generated tweet to Twitter
    post_tweet(tweet)

if __name__ == "__main__":
    main()