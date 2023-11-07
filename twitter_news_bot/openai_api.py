from urllib import response
import openai
from datetime import datetime
from nltk.tokenize import sent_tokenize
import logging
import json
import os
import traceback
import boto3


# Initialize logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    event_body = event  # Directly use the event as the event_body, no need for json.loads

    # Check for a dictionary type for event_body
    if isinstance(event_body, dict):
        article_data = event_body.get('article_data', {})
    else:
        logger.error("Event body is not a dictionary.")
        article_data = {}

    title = article_data.get('title', 'N/A')  # This line remains unchanged
    openai_api_key = os.environ.get('OPENAI_API_KEY')  # This line remains unchanged

    try:
        generated_tweet = generate_tweet(article_data, openai_api_key) if article_data else None
        if generated_tweet:
            logger.info(f"Successfully generated tweet: {generated_tweet}")

            # Check if running offline
            lambda_port = 3002 if os.environ.get('IS_OFFLINE') else None
            endpoint_url = f'http://localhost:{lambda_port}' if lambda_port else None

            # Initialize Lambda client
            lambda_client = boto3.client('lambda', endpoint_url=endpoint_url) if endpoint_url else boto3.client('lambda')

            # Function name from serverless.yaml
            functionName = 'cannabis-news-bot-dev-postTweet' if lambda_port else 'postTweet'

            # Prepare the payload for twitter_api.py Lambda function
            payload = {
                'tweet_content': generated_tweet
            }

            # Invoke twitter_api.py Lambda function asynchronously
            lambda_client.invoke(
                FunctionName=functionName,  # Make sure this matches the actual name of the deployed Lambda function
                InvocationType='Event',
                Payload=json.dumps(payload)
            )
            
            logger.info("Lambda handler has finished executing and is about to return success response")  # Additional log
            
            response = {
                'statusCode': 200,
                'body': json.dumps({'message': 'Success'})
            }
            logger.info(f"About to return from lambda_handler: {response}")
            return response

    except Exception as e:
        logger.error(f"Failed to generate tweet: {str(e)}")
        traceback.print_exc()  # Log the traceback
        logger.info("About to return failure response from lambda_handler")  # Additional log
        return {
            'statusCode': 500,
            'body': json.dumps('Failed')
        }

def generate_tweet(article_data, openai_api_key, max_tweet_length=280):
    logger.debug(f"Received article data: {article_data}")
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
            model="gpt-4-1106-preview",
            messages=messages,
            temperature=0.5,
            max_tokens=content_max_tokens
        )

        # Log the raw response from OpenAI
        logger.debug(f"OpenAI raw response: {response.choices[0].message}")

        # Post-process generated tweet
        generated_tweet = response.choices[0].message['content'].strip()
        logger.debug(f"Generated Tweet: {generated_tweet}")

        # Assemble the full tweet
        full_tweet = f"{generated_tweet}\nurl: {article_data['url']}\nSentiment: {article_data['sentiment']}\nTopic: {article_data['topic']}\n#Cannabis #Marijuana"

        # Handle tweet length
        while len(full_tweet) > max_tweet_length:
            # Tokenize into sentences
            sentences = sent_tokenize(generated_tweet)
            del sentences[-1]  # Remove the last sentence
            generated_tweet = ' '.join(sentences)

            # Reassemble the tweet
            full_tweet = f"{generated_tweet}\nurl: {article_data['url']}\nSentiment: {article_data['sentiment']}\nTopic: {article_data['topic']}\n#Cannabis #Marijuana"

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
        traceback.print_exc()
        return None
