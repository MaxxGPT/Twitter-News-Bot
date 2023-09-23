import os
import openai
import tweepy
import random
import requests
import re
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
twitter_bearer_token = os.getenv("TWITTER_BEARER_TOKEN")

# Initialize Twitter API client
twitter_api = tweepy.Client(twitter_bearer_token, twitter_consumer_key, twitter_consumer_secret, twitter_access_token, twitter_access_token_secret, wait_on_rate_limit=False)

def fetch_news_articles(max_retries=5):
    params = {"limit": 100}
    headers = {'Accept': 'application/json', 'apikey': cannabis_news_api_key}
    retries = 0  # Initialize retry counter

    while retries < max_retries:
        try:
            response = requests.get(cannabis_news_endpoint, params=params, headers=headers)
            response.raise_for_status()  # Raise an exception for HTTP error

            if response.status_code == 200:
                json_response = response.json()
                articles = json_response['articles']

                cannabis_keywords = ["cannabis", "marijuana", "weed", "THC", "CBD", "hemp", "pot", "stoned", "stoner", "420", "4/20", "4:20", "bong", "high", "drug", "drugs"]

                cannabis_articles = [
                    article for article in articles
                    if any(
                        keyword.lower() in (article.get(field) or '').lower()
                        for keyword in cannabis_keywords
                        for field in ['title', 'description']
                    )
                ]

                if cannabis_articles:
                    article = random.choice(cannabis_articles)
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
                        "summarization": article['summarization'],
                        "GPE": article['GPE'],
                        "ORG": article['ORG'],
                        "PERSON": article['PERSON'],
                    }
                    return article_data

            else:
                print("Failed to retrieve articles. Status Code:", response.status_code)
                return None

        except requests.exceptions.RequestException as e:
            print("Error fetching news articles:", e)
            return None

        retries += 1
        print(f"No cannabis-related articles found in batch {retries}. Retrying...")

    print(f"Exhausted maximum retries ({max_retries}) without finding a cannabis-related article.")
    return None

def generate_tweet(article_data):
    topic_hashtag_map = {
        "Business": "#Business",
        "Crime": "#Crime",
        "Politics": "#Politics",
        "Consumer": "#Consumer"
    }
    topic_hashtag = topic_hashtag_map.get(article_data['topic'], "")
    system_message = "You're a digital cannabis news reporter and your task is to create an engaging tweet about a recent article."
    user_message = (f"Start with a hook or the article's title to grab attention. Provide a snippet or your take on the news. "
                    f"Encourage people to read the full story using the URL. And remember to let them know the sentiment and topic of the article.\n"
                    f"Title: {article_data['title']}\nURL: {article_data['url']}\nSentiment: {article_data['sentiment']}\nTopic: {article_data['topic']}")

    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_message}
    ]

    max_tweet_length = 280
    while True:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages,
            temperature=0.7,
            max_tokens=90
        )
        generated_tweet = response.choices[0].message['content'].strip()
        generated_tweet = re.sub(r"#\w+", "", generated_tweet)
        generated_tweet += f"\nSentiment: {article_data['sentiment']}\nTopic: {article_data['topic']}"
        generated_tweet = generated_tweet.replace(article_data['topic'], topic_hashtag)
        generated_tweet += "\n#Cannabis #Weed"

        if len(generated_tweet) <= max_tweet_length:
            return generated_tweet


def post_tweet(tweet_content):
    try:
        response = twitter_api.create_tweet(text=tweet_content)
        print("Tweet posted successfully:", tweet_content)
    except tweepy.errors.TweepyException as e:
        print("Error posting tweet:", e)

def main():
    article_data = fetch_news_articles()
    if article_data:
        tweet = generate_tweet(article_data)
        print("Generated Tweet:")
        print(tweet)
        post_tweet(tweet)

if __name__ == "__main__":
    main()
