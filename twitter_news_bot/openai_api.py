import openai
from datetime import datetime
from nltk.tokenize import sent_tokenize
import logging

logger = logging.getLogger(__name__)

def generate_tweet(article_data, openai_api_key, max_tweet_length=280):
    try:
        logger.info(f"{datetime.now()} - Starting to generate tweet...")

        # Initialize OpenAI API key
        openai.api_key = openai_api_key

        # Calculate maximum length for generatable content
        content_max_tokens = max_tweet_length // 4  # Adjust as needed
        
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

        # Assemble the full tweet
        full_tweet = f"{generated_tweet}\nUrl: {article_data['url']}\nSentiment: {article_data['sentiment']}\nTopic: {article_data['topic']}\n#Cannabis #Marijuana"

        # Handle tweet length
        while len(full_tweet) > max_tweet_length:
            # Tokenize into sentences
            sentences = sent_tokenize(generated_tweet)
            del sentences[-1]  # Remove the last sentence
            generated_tweet = ' '.join(sentences)

            # Reassemble the tweet
            full_tweet = f"{generated_tweet}\nUrl: {article_data['url']}\nSentiment: {article_data['sentiment']}\nTopic: {article_data['topic']}\n#Cannabis #Marijuana"

        logger.info(f"Generated tweet length: {len(full_tweet)}")
        logger.info(f"Generated tweet content: {full_tweet}")

        if len(full_tweet) <= max_tweet_length:
            logger.info(f"{datetime.now()} - Finished generating tweet.")
            return full_tweet
        else:
            logger.warning(f"{datetime.now()} - Generated tweet is still too long after truncation. Retrying...")
            return None

    except Exception as e:
        logger.error(f"Failed to generate tweet: {e}")
        return None
