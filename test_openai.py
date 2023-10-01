import os
import openai
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI API credentials
openai.api_key = os.getenv("OPENAI_API_KEY")

# Dummy article data for testing
article_data = {
    "title": "Example Title",
    "url": "https://example.com",
    "sentiment": "Positive",
    "topic": "Business"
}

def generate_tweet(article_data):
    print(f"Starting OpenAI API call at {datetime.now()}")
    
    topic_hashtag_map = {
        "Business": "#Business",
        "Crime": "#Crime",
        "Politics": "#Politics",
        "Consumer": "#Consumer"
    }
    topic_hashtag = topic_hashtag_map.get(article_data['topic'], "")
    system_message = "You're a digital cannabis news reporter and your task is to create an engaging tweet about a recent article."
    user_message = f"Start with a hook or the article's title to grab attention. Provide a snippet or your take on the news. Encourage people to read the full story. Do not shorten the url, and remember to let them know the sentiment and topic of the article.\nTitle: {article_data['title']}\nURL: {article_data['url']}\nSentiment: {article_data['sentiment']}\nTopic: {article_data['topic']}"
    
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_message}
    ]
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages,
            temperature=0.7,
            max_tokens=90
        )
        generated_tweet = response.choices[0].message['content'].strip()
        print(f"Generated Tweet: {generated_tweet}")
        print(f"OpenAI API call completed at {datetime.now()}")
        
    except Exception as e:
        print(f"An error occurred: {e}")
        print(f"Error occurred at {datetime.now()}")

if __name__ == "__main__":
    generate_tweet(article_data)
