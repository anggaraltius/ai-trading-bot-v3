import pandas as pd
import pandas_ta as ta
from analyzer import Analyzer
from data_fetcher import DataFetcher
from risk_management import RiskManagement
import numpy as np

class Backtester:

    def __init__(self, balance=1000, risk_per_trade=0.02, sl_buffer=0.01, rr_ratio=2.0):
        self.balance = balance
        self.risk_per_trade = risk_per_trade
        self.sl_buffer = sl_buffer
        self.rr_ratio = rr_ratio

    def backtest(self, symbol, mode, interval, limit=1000):
        df = DataFetcher.get_binance_klines(symbol, interval, limit=limit)
        df = Analyzer.apply_indicators(df, mode)

        results = []
        rm = RiskManagement(self.balance, self.risk_per_trade, self.sl_buffer, self.rr_ratio)

        for i in range(50, len(df)):
            data_slice = df.iloc[:i+1]
            signal = Analyzer.generate_signal(data_slice, mode)
            current_price = data_slice.iloc[-1]['close']

            if signal == 'BUY':
                plan = rm.generate_trade_plan(current_price)
                profit = plan['Take Profit'] - plan['Entry Price']
                loss = plan['Entry Price'] - plan['Stop Loss']
                outcome = np.random.choice(['TP', 'SL'], p=[0.5, 0.5])

                if outcome == 'TP':
                    gain = profit * plan['Position Size']
                else:
                    gain = -loss * plan['Position Size']

                results.append(gain)

        return self.analyze_results(results)

    def analyze_results(self, results):
        if not results:
            return {"Total Trades": 0}

        total = sum(results)
        win = sum(1 for r in results if r > 0)
        loss = sum(1 for r in results if r < 0)
        winrate = win / len(results)
        profit_factor = (sum(r for r in results if r > 0) / abs(sum(r for r in results if r < 0))) if loss > 0 else float('inf')
        max_dd = self.max_drawdown(results)

        return {
            "Total Trades": len(results),
            "Win Trades": win,
            "Loss Trades": loss,
            "Winrate": round(winrate * 100, 2),
            "Profit Factor": round(profit_factor, 2),
            "Max Drawdown": round(max_dd, 2),
            "Total Profit USD": round(total, 2)
        }

    def max_drawdown(self, results):
        equity = [self.balance]
        for r in results:
            equity.append(equity[-1] + r)
        equity_curve = pd.Series(equity)
        drawdown = equity_curve - equity_curve.cummax()
        max_dd = drawdown.min()
        return max_dd
