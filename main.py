import logging
from twitter_news_bot.config import load_config, initialize_twitter_api  
from twitter_news_bot.data_fetcher import fetch_news_articles
from twitter_news_bot.data_updater import mark_as_tweeted
from twitter_news_bot.openai_api import generate_tweet
from twitter_news_bot.twitter_api import post_tweet  
from twitter_news_bot.logger import setup_logger

# Initialize the logger
setup_logger()
logger = logging.getLogger(__name__)

def main():
    try:
        # Load the configuration
        config = load_config()

        # Initialize the Twitter API once
        twitter_api = initialize_twitter_api()

        # Fetch a news article
        article_data = fetch_news_articles(
            config['cannabis_news_api_key'], 
            config['CANNABIS_NEWS_ENDPOINT'], 
            int(config['max_retries']), 
            int(config['max_total_attempts'])
        )
        
        if not article_data:
            logger.warning("No article data received.")
            return
        else:
            logger.info(f"Retrieved article with ID: {article_data['_id']}")
            logger.info(f"Successfully retrieved article data: {article_data}")

        # Generate a tweet based on the article
        tweet = generate_tweet(article_data, config['OPENAI_API_KEY'])
        
        if not tweet:
            logger.warning("Tweet generation failed.")
            return
        else:
            logger.info(f"Successfully generated tweet: {tweet}")

        # Post the tweet
        post_tweet(tweet, twitter_api)  # Pass the initialized Twitter API here

        # Mark the article as tweeted in the database
        mark_as_tweeted(article_data["_id"], config['cannabis_news_api_key'], config['CANNABIS_NEWS_UPDATE_ENDPOINT'])

    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}", exc_info=True)  # exc_info=True will log the traceback

if __name__ == "__main__":
    main()
