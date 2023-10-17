import unittest
from unittest.mock import MagicMock
from unittest.mock import patch
from twitter_news_bot.openai_api import generate_tweet

class TestGenerateTweet(unittest.TestCase):
    
    @patch('openai.ChatCompletion.create')
    def test_generate_tweet_success(self, mock_openai_create):
        # Mock the response from OpenAI API
        mock_choice = MagicMock()
        mock_choice.message = {'content': 'Great article!'}

        mock_response = MagicMock()
        mock_response.choices = [mock_choice]

        mock_openai_create.return_value = mock_response
        
        article_data = {
            'title': 'New Cannabis Law',
            'sentiment': 'Positive',
            'topic': 'Legalization',
            'url': 'https://example.com/article'
        }

        # Call the function
        result = generate_tweet(article_data, 'fake_openai_api_key')
        
        # Check if the tweet is generated successfully
        self.assertIsNotNone(result)
        self.assertTrue('Great article!' in result)
        
    @patch('openai.ChatCompletion.create')
    def test_generate_tweet_failure(self, mock_openai_create):
        # Mock the response to throw an exception
        mock_openai_create.side_effect = Exception("API call failed")
        
        article_data = {
            'title': 'New Cannabis Law',
            'sentiment': 'Positive',
            'topic': 'Legalization',
            'url': 'https://example.com/article'
        }

        # Call the function
        result = generate_tweet(article_data, 'fake_openai_api_key')
        
        # Check if the tweet generation failed
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
