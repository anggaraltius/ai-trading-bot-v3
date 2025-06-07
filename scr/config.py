import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    COHERE_API_KEY = os.getenv("COHERE_API_KEY")
    ALPHAVANTAGE_API_KEY = os.getenv("ALPHAVANTAGE_API_KEY")
    NEWSAPI_API_KEY = os.getenv("NEWSAPI_API_KEY")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    BINANCE_BASE_URL = 'https://api.binance.com'
