import requests
import random
from datetime import datetime
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def fetch_single_article(source_id, api_key, endpoint):
    params = {"limit": 1, "source_id": source_id}
    headers = {'Accept': 'application/json', 'apikey': api_key}

    try:
        response = requests.get(endpoint, params=params, headers=headers)
        response.raise_for_status()

        if response.status_code == 200:
            json_response = response.json()
            articles = json_response['articles']
            if articles:
                article = articles[0]
                return {
                    "title": article['title'],
                    "url": article['url'],
                    "topic": article['Topic'],
                    "sentiment": article['sentiment'],
                }
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching news articles: {e}")
    return None

def fetch_news_articles(api_key, endpoint, max_retries=5, max_total_attempts=50):
    logger.info("Starting to fetch articles...")

    # Your list of source_ids
    source_ids = [
        "420-intel", "canna-law-blog", "cannabis-business-times", "green-entrepreneurs", 
        "new-cannabis-ventures", "pot-network", "the-fresh-toast", "420-magazine", 
        "cannabis-culture", "cannverse-solutions", "hail-mary-jane", "hemp-industry-daily", 
        "leafly", "marijuana-moment", "marley-natural", "merry-jane", "the-growth-op", 
        "california-weed-blog", "cannabis-watch", "leafbuyer", "marijuana-business-daily", 
        "the-cannabist", "cannabis-law-report", "cannabis-life-network", "high-times", 
        "marijuana", "marijuana-politics", "mg-retailer", "the-joint-blog", "weedmaps", "leafwell"
    ]

    total_attempts = 0  # Initialize total_attempts counter
    
    while total_attempts < max_total_attempts:
        specific_source_id = random.choice(source_ids)  # Randomly select a source
        retries = 0  # Reset retries counter for each source
        
        while retries < max_retries:
            total_attempts += 1  # Increment total_attempts counter
            
            article_data = fetch_single_article(specific_source_id, api_key, endpoint)
            if article_data:
                logger.info("Finished fetching articles.")
                return article_data

            retries += 1
            logger.warning(f"No articles found in batch {retries}. Retrying...")
            
        logger.warning(f"Exhausted maximum retries ({max_retries}) for source {specific_source_id}. Moving to next source...")
        
    logger.error(f"Exhausted maximum total attempts ({max_total_attempts}) without finding an article.")
    return None
