from twitter_news_bot.config import load_config, initialize_twitter_api  # Import initialize_twitter_api
from twitter_news_bot.data_fetcher import fetch_news_articles
from twitter_news_bot.openai_api import generate_tweet
from twitter_news_bot.twitter_api import post_tweet  # Make sure this import works
from twitter_news_bot.utils import log_message

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
            log_message("No article data received.")
            return
        else:
            log_message(f"Successfully retrieved article data: {article_data}")

        # Generate a tweet based on the article
        tweet = generate_tweet(article_data, config['OPENAI_API_KEY'])
        
        if not tweet:
            log_message("Tweet generation failed.")
            return
        else:
            log_message(f"Successfully generated tweet: {tweet}")

        # Post the tweet
        post_tweet(tweet, twitter_api)  # Pass the initialized Twitter API here

    except Exception as e:
        log_message(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
