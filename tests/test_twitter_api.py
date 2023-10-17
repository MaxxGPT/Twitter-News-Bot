import unittest
from unittest.mock import MagicMock
from twitter_news_bot.twitter_api import calculate_tweet_length, post_tweet

class TestTweetFunctions(unittest.TestCase):

    def test_post_tweet_success(self):
        mock_twitter_api = MagicMock()
        mock_twitter_api.create_tweet.return_value = 'some_response'
        
        with self.assertLogs(level='INFO') as cm:
            post_tweet('Test tweet', mock_twitter_api)
        
        self.assertIn('Tweet posted successfully: Test tweet', cm.output[0])

    def test_post_tweet_failure(self):
        mock_twitter_api = MagicMock()
        mock_twitter_api.create_tweet.side_effect = Exception('API Error')
        
        with self.assertLogs(level='ERROR') as cm:
            post_tweet('Test tweet', mock_twitter_api)
        
        self.assertIn('An unexpected error occurred: API Error', cm.output[0])
        self.assertIn("Exception type: <class 'Exception'>", cm.output[1])

if __name__ == '__main__':
    unittest.main()
