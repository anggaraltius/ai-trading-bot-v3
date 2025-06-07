import requests
import datetime
import os
import cohere
from config import Config
from llm_sentiment import LLMSentiment

class SentimentAnalyzer:

    def __init__(self, model='gpt'):
        self.model = model
        self.cohere_client = cohere.Client(Config.COHERE_API_KEY)
        self.llm_client = LLMSentiment()

    def fetch_news(self, query: str, from_days_ago: int = 2, language='en', page_size=20):
        url = 'https://newsapi.org/v2/everything'
        from_date = (datetime.datetime.now() - datetime.timedelta(days=from_days_ago)).strftime('%Y-%m-%d')

        params = {
            'q': query,
            'from': from_date,
            'language': language,
            'sortBy': 'relevancy',
            'pageSize': page_size,
            'apiKey': Config.NEWSAPI_API_KEY
        }
        response = requests.get(url, params=params)
        data = response.json()
        return [article['title'] for article in data.get('articles', [])]

    def analyze_sentiment_cohere(self, texts: list):
        if not texts:
            return "Neutral"
        
        sentiment_labels = []
        for text in texts:
            response = self.cohere_client.classify(
                model='large',
                inputs=[text],
                examples=[
                    ["Bitcoin price is surging rapidly!", "Positive"],
                    ["Ethereum faces massive sell-off", "Negative"],
                    ["Market remains stable for now", "Neutral"],
                    ["Big bullish breakout on Binance", "Positive"],
                    ["Crypto crash causes panic", "Negative"],
                    ["Investors are optimistic about new ETF", "Positive"],
                    ["Major hack wipes billions", "Negative"]
                ]
            )
            label = response.classifications[0].prediction
            sentiment_labels.append(label)

        score = {"Positive": 0, "Neutral": 0, "Negative": 0}
        for label in sentiment_labels:
            score[label] += 1

        final_sentiment = max(score, key=score.get)
        return final_sentiment

    def get_overall_sentiment(self, query: str):
        news_titles = self.fetch_news(query)
        if self.model == 'cohere':
            sentiment = self.analyze_sentiment_cohere(news_titles)
        elif self.model == 'gpt':
            sentiment = self.llm_client.analyze_sentiment(news_titles)
        else:
            sentiment = "Neutral"
        return sentiment
