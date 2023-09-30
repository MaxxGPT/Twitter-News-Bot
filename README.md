# Twitter Bot for Cannabis News #

### Overview ###

This Twitter bot is designed to automatically post tweets related to cannabis news. It fetches news articles from a cannabis news API, generates a tweet using OpenAI's GPT-4 model, and then posts it to Twitter.

### Version ###

1.0.0

### Features ###

* Fetches cannabis-related news articles.
* Generates tweets based on the fetched news articles.
* Automatically posts tweets to Twitter.

### Prerequisites ###

* Python 3.x
* pip
* Twitter Developer Account
* OpenAI API key

### Installation ###

## Clone the repository ##

```
git clone git@bitbucket.org:VueMongo/twitter-news-bot.git

```

## Install Dependencies ##

```
pip install -r requirements.txt

```

## Environment Variables ##

Create a .env file in the root directory and populate it with the necessary API keys and tokens:
```
OPENAI_API_KEY=your_openai_api_key
CANNABISNEWSAPIKEY=your_cannabis_news_api_key
TWITTER_CONSUMER_KEY=your_twitter_consumer_key
TWITTER_CONSUMER_SECRET=your_twitter_consumer_secret
TWITTER_ACCESS_TOKEN=your_twitter_access_token
TWITTER_ACCESS_TOKEN_SECRET=your_twitter_access_token_secret
TWITTER_BEARER_TOKEN=your_twitter_bearer_token
```

### Usage ###

To run the Twitter bot:

```
python main.py

```

### Contributing ###

1. Fork the repository
2. Create a new branch (git checkout -b feature-branch).
3. Commit your changes (git commit -am 'Add new feature').
4. Push to the branch (git push origin feature-branch).
5. Create a new Pull Request. 
