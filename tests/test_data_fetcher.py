import unittest
from twitter_news_bot.data_fetcher import fetch_news_articles, mark_as_tweeted, fetch_single_article
from unittest.mock import patch

class TestDataFetcher(unittest.TestCase):
    
    @patch('requests.patch')
    def test_mark_as_tweeted_success(self, mock_patch):
        mock_patch.return_value.status_code = 200
        result = mark_as_tweeted('some_id', 'some_key', 'some_endpoint/{id}')
        self.assertEqual(result, True)
    
    @patch('requests.get')
    def test_fetch_single_article_success(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {'articles': [{'_id': 'some_id', 'title': 'some_title', 'url': 'some_url', 'Topic': 'some_topic', 'sentiment': 'some_sentiment'}]}   
        result = fetch_single_article('some_source', 'some_key', 'some_endpoint')
        self.assertIsNotNone(result)
        
    @patch('twitter_news_bot.data_fetcher.fetch_single_article')
    def test_fetch_news_articles_success(self, mock_fetch_single):
        mock_fetch_single.return_value = {'_id': 'some_id'}
        result = fetch_news_articles('some_key', 'some_endpoint')
        self.assertIsNotNone(result)

if __name__ == '__main__':
    unittest.main()
