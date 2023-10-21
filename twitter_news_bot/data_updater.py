import requests
import random
from datetime import datetime
import logging

# Initialize logging
logger = logging.getLogger(__name__)

def mark_as_tweeted(article_id, api_key, update_endpoint):
    """
    Mark a specific article as tweeted in the database.
    """
    headers = {'Accept': 'application/json', 'apiKey': api_key, 'Content-Type': 'application/json'}
    
    data = {"tweeted": True}

    formatted_url = update_endpoint.format(id=article_id)

    logger.debug(f"Headers for marking as tweeted: {headers}")
    logger.debug(f"URL for marking as tweeted: {formatted_url}")

    
    try:
        response = requests.patch(formatted_url, headers=headers, json=data)
        response = requests.patch(update_endpoint.format(id=article_id), headers=headers, json=data)

        if response.status_code == 200:
            logger.info(f"Successfully marked article with ID {article_id} as tweeted.")
            return True
        else:
            logger.warning(f"Failed to mark article with ID {article_id} as tweeted. Response code: {response.status_code}")
            return False
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Error updating 'tweeted' status for article with ID {article_id}: {e}")