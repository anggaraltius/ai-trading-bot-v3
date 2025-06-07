import requests
import pandas as pd
from config import Config

class DataFetcher:
    @staticmethod
    def get_binance_klines(symbol, interval, limit=200):
        url = f"{Config.BINANCE_BASE_URL}/api/v3/klines"
        params = {"symbol": symbol, "interval": interval, "limit": limit}
        response = requests.get(url, params=params)
        data = response.json()
        df = pd.DataFrame(data, columns=["open_time", "open", "high", "low", "close", "volume",
                                          "close_time", "quote_asset_volume", "number_of_trades",
                                          "taker_buy_base_vol", "taker_buy_quote_vol", "ignore"])
        df["close"] = df["close"].astype(float)
        df["open"] = df["open"].astype(float)
        df["high"] = df["high"].astype(float)
        df["low"] = df["low"].astype(float)
        df["volume"] = df["volume"].astype(float)
        return df
