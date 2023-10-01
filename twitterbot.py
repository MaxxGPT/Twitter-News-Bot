import os
import openai
import tweepy
import random
import requests
import re
from dotenv import load_dotenv
from time import sleep
from datetime import datetime
from nltk.tokenize import sent_tokenize


# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI, Cannabis News API, and Twitter API credentials
openai.api_key = os.getenv("OPENAI_API_KEY")
cannabis_news_api_key = os.getenv("CANNABISNEWSAPIKEY")
cannabis_news_endpoint = os.getenv("CANNABIS_NEWS_ENDPOINT")
twitter_consumer_key = os.getenv("TWITTER_CONSUMER_KEY")
twitter_consumer_secret = os.getenv("TWITTER_CONSUMER_SECRET")
twitter_access_token = os.getenv("TWITTER_ACCESS_TOKEN")
twitter_access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
twitter_bearer_token = os.getenv("TWITTER_BEARER_TOKEN")

# Initialize Twitter API client
twitter_api = tweepy.Client(twitter_bearer_token, twitter_consumer_key, twitter_consumer_secret, twitter_access_token, twitter_access_token_secret, wait_on_rate_limit=True)

def calculate_tweet_length(tweet):
    url_count = tweet.count('http')
    return len(tweet) + (url_count * (23 - 6))  # Twitter counts URLs as 23 characters

# Function to fetch cannabis-related news articles
def fetch_news_articles(max_retries=5, specific_source_id='new-cannabis-ventures'):
    print(f"{datetime.now()} - Starting to fetch articles...")
    
    params = {"limit": 1, "source_id": specific_source_id}  # Limit set to 1, as you want the first article only
    headers = {'Accept': 'application/json', 'apikey': cannabis_news_api_key}
    retries = 0  # Initialize retry counter

    while retries < max_retries:
        try:
            response = requests.get(cannabis_news_endpoint, params=params, headers=headers)
            response.raise_for_status()
            if response.status_code == 200:
                json_response = response.json()
                articles = json_response['articles']

                if articles:
                    article = articles[0]  # Taking the first article as you mentioned
                    article_data = {
                        "title": article['title'],
                        "url": article['url'],
                        "topic": article['Topic'],
                        "sentiment": article['sentiment'],
                    }
                    print(f"{datetime.now()} - Finished fetching articles.")
                    return article_data
            else:
                print(f"{datetime.now()} - Failed to retrieve articles. Status Code: {response.status_code}")
                return None
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:
                print(f"{datetime.now()} - Rate limit reached for Cannabis News API. Waiting...")
                sleep(60)
            else:
                print(f"{datetime.now()} - An HTTP error occurred: {e}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"{datetime.now()} - Error fetching news articles: {e}")
            return None

        retries += 1
        print(f"{datetime.now()} - No articles found in batch {retries}. Retrying...")
        
    print(f"{datetime.now()} - Exhausted maximum retries ({max_retries}) without finding an article.")
    return None


# Function to generate a tweet based on an article

def generate_tweet(article_data):
    print(f"{datetime.now()} - Starting to generate tweet...")
    
    # Fixed components
    constant_labels_length = len("Url: Sentiment: Topic: ")
    constant_hashtags_length = len("#Cannabis #Marijuana")
    fixed_components_length = constant_labels_length + constant_hashtags_length
    max_tweet_length = 280
    
    # Dynamic components for each tweet
    dynamic_components = f"{article_data['url']} {article_data['sentiment']} {article_data['topic']}"
    dynamic_components_length = len(dynamic_components)

    # Calculate maximum length for generatable content
    max_generatable_length = max_tweet_length - (fixed_components_length + dynamic_components_length)
    content_max_tokens = max_generatable_length // 4  # Adjust as needed
    
    system_message = "You're a digital cannabis news reporter and your task is to create an engaging tweet about a recent article."
    user_message = f"Start with a hook or the article's title to grab attention. Provide a snippet or your take on the news.\nTitle: {article_data['title']}\nSentiment: {article_data['sentiment']}\nTopic: {article_data['topic']}"
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_message}
    ]
    
    # OpenAI API call
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
        temperature=0.5,
        max_tokens=content_max_tokens
    )

    # Post-process generated tweet
    generated_tweet = response.choices[0].message['content'].strip()

    # Assemble the full tweet with URL, sentiment, etc.
    full_tweet = f"{generated_tweet}\nUrl: {article_data['url']}\nSentiment: {article_data['sentiment']}\nTopic: {article_data['topic']}\n#Cannabis #marijuana"

    # Check if the tweet is too long
    if len(full_tweet) > max_tweet_length:
        # Tokenize into sentences
        sentences = sent_tokenize(generated_tweet)
        
        # Attempt to keep essential information (e.g., first sentence)
        essential_info = sentences[0]
        
        # Start removing extra sentences from the end
        while len(full_tweet) > max_tweet_length and len(sentences) > 1:
            del sentences[-1]
            truncated_tweet = ' '.join(sentences)
            
            # Reassemble the tweet
            full_tweet = f"{truncated_tweet}\nUrl: {article_data['url']}\nSentiment: {article_data['sentiment']}\nTopic: {article_data['topic']}\n#Cannabis #marijuana"

        # If still too long, try to shorten words or use abbreviations
        if len(full_tweet) > max_tweet_length:
            # Implement your logic to shorten words or use abbreviations
            # For example: Replace 'million' with 'M', 'business' with 'biz', etc.
            pass  # Replace this with your actual implementation

    print(f"Generated tweet length: {len(full_tweet)}")
    print(f"Generated tweet content: {full_tweet}")

    if len(full_tweet) <= max_tweet_length:
        print(f"{datetime.now()} - Finished generating tweet.")
        return full_tweet
    else:
        print(f"{datetime.now()} - Generated tweet is still too long after truncation. Retrying...")
        return None




# Function to post the generated tweet
def post_tweet(tweet_content):
    try:
        response = twitter_api.create_tweet(text=tweet_content)
        print("Tweet posted successfully:", tweet_content)
    except Exception as e:  # Catch all exceptions
        print(f"An unexpected error occurred: {e}")
        print(f"Exception type: {type(e)}")


# Main function to control the flow of the script
def main():
    # Try to fetch an article, generate a tweet, and post it
    try:
        article_data = fetch_news_articles()
        if article_data:
            tweet = generate_tweet(article_data)
            if tweet:
                print("Generated Tweet:")
                print(tweet)
                post_tweet(tweet)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


# Entry point of the script
if __name__ == "__main__":
    main()
