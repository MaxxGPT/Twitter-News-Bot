from twitter_news_bot.config import load_config
from twitter_news_bot.data_fetcher import fetch_news_articles
from twitter_news_bot.openai_api import generate_tweet  # Add this line
from twitter_news_bot.utils import log_message

def main():
    try:
        # Load the configuration
        config = load_config()

        # Fetch a news article
        article_data = fetch_news_articles(
            config['cannabis_news_api_key'], 
            config['CANNABIS_NEWS_ENDPOINT'], 
            int(config['max_retries']), 
            int(config['max_total_attempts'])
        )
        
        if not article_data:
            log_message("No article data received.")
            return
        else:
            log_message(f"Successfully retrieved article data: {article_data}")

        # Generate a tweet based on the article
        tweet = generate_tweet(article_data, config['OPENAI_API_KEY'])  # Add this line
        if not tweet:
            log_message("Tweet generation failed.")
            return
        else:
            log_message(f"Successfully generated tweet: {tweet}")  # Add this line

    except Exception as e:
        log_message(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
