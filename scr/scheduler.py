from apscheduler.schedulers.background import BackgroundScheduler
from data_fetcher import DataFetcher
from analyzer import Analyzer
from pattern_detector import PatternDetector
from sentiment_analyzer import SentimentAnalyzer
from risk_management import RiskManagement
import logging

class SignalScheduler:

    def __init__(self, bot_interface):
        self.bot = bot_interface
        self.scheduler = BackgroundScheduler()
        self.sentiment = SentimentAnalyzer(model='gpt')
        self.default_account_balance = 1000
        self.risk_engine = RiskManagement(account_balance=self.default_account_balance)

    def start(self):
        self.scheduler.start()

    def add_job(self, chat_id, symbol, mode, interval):
        self.scheduler.add_job(
            self.run_analysis,
            'interval',
            seconds=interval,
            args=[chat_id, symbol, mode],
            id=f"{chat_id}-{symbol}-{mode}",
            replace_existing=True
        )
        logging.info(f"Job added: {chat_id} {symbol} {mode}")

    def remove_job(self, chat_id, symbol, mode):
        job_id = f"{chat_id}-{symbol}-{mode}"
        self.scheduler.remove_job(job_id)
        logging.info(f"Job removed: {job_id}")

    def run_analysis(self, chat_id, symbol, mode):
        try:
            interval_map = {
                "scalper": "1m",
                "intraday": "1h",
                "swing": "4h"
            }
            df = DataFetcher.get_binance_klines(symbol, interval_map[mode])
            df = Analyzer.apply_indicators(df, mode)
            signal = Analyzer.generate_signal(df, mode)
            patterns = PatternDetector.detect_patterns(df)
            sentiment = self.sentiment.get_overall_sentiment(symbol.replace("USDT", ""))
            current_price = df.iloc[-1]['close']

            message = f"🔔 Signal for {symbol} ({mode.upper()})\n"
            message += f"Signal: {signal}\n"
            message += f"Pattern: {', '.join(patterns) if patterns else 'No pattern'}\n"
            message += f"Sentiment: {sentiment}\n"

            if signal in ['BUY', 'SELL']:
                risk_plan = self.risk_engine.generate_trade_plan(entry_price=current_price)
                message += "\n💰 Trade Plan:\n"
                message += f"Entry: {risk_plan['Entry Price']}\n"
                message += f"Position Size: {risk_plan['Position Size']} {symbol[:-4]}\n"
                message += f"Stop Loss: {risk_plan['Stop Loss']}\n"
                message += f"Take Profit: {risk_plan['Take Profit']}\n"
                message += f"Risk Amount: ${risk_plan['Risk Amount (USD)']}\n"

            self.bot.send_message(chat_id, message)

        except Exception as e:
            logging.error(f"Error running analysis: {e}")
            self.bot.send_message(chat_id, f"Error analyzing {symbol}: {str(e)}")
