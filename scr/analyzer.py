import pandas as pd
import pandas_ta as ta

class Analyzer:

    @staticmethod
    def apply_indicators(df: pd.DataFrame, mode: str):
        if mode == 'scalper':
            df['ema9'] = ta.ema(df['close'], length=9)
            df['ema20'] = ta.ema(df['close'], length=20)
            df['rsi'] = ta.rsi(df['close'], length=14)
            df['stochrsi'] = ta.stochrsi(df['close'], length=14)
        elif mode == 'intraday':
            df['ema50'] = ta.ema(df['close'], length=50)
            df['ema200'] = ta.ema(df['close'], length=200)
            macd = ta.macd(df['close'])
            df['macd'] = macd['MACD_12_26_9']
            df['macd_signal'] = macd['MACDs_12_26_9']
            df['rsi'] = ta.rsi(df['close'], length=14)
        elif mode == 'swing':
            df['ema50'] = ta.ema(df['close'], length=50)
            df['ema200'] = ta.ema(df['close'], length=200)
            df['rsi'] = ta.rsi(df['close'], length=14)
        else:
            raise ValueError("Mode tidak dikenali")
        return df

    @staticmethod
    def calculate_fibonacci_zone(df: pd.DataFrame):
        recent = df.tail(50)
        high = recent['high'].max()
        low = recent['low'].min()
        level_382 = high - (high - low) * 0.382
        level_618 = high - (high - low) * 0.618
        lower_bound = min(level_382, level_618)
        upper_bound = max(level_382, level_618)
        return lower_bound, upper_bound

    @staticmethod
    def generate_signal(df: pd.DataFrame, mode: str) -> str:
        signal = "NO SIGNAL"
        last = df.iloc[-1]
        price = last['close']

        if mode == 'scalper':
            if last['ema9'] > last['ema20'] and last['rsi'] < 70:
                signal = "BUY"
            elif last['ema9'] < last['ema20'] and last['rsi'] > 30:
                signal = "SELL"

        elif mode in ['intraday', 'swing']:
            fib_low, fib_high = Analyzer.calculate_fibonacci_zone(df)
            if not (fib_low <= price <= fib_high):
                return "NO SIGNAL (Outside Fib Zone)"
            if mode == 'intraday':
                if last['ema50'] > last['ema200'] and last['macd'] > last['macd_signal']:
                    signal = "BUY"
                elif last['ema50'] < last['ema200'] and last['macd'] < last['macd_signal']:
                    signal = "SELL"
            elif mode == 'swing':
                if last['ema50'] > last['ema200'] and last['rsi'] < 70:
                    signal = "BUY"
                elif last['ema50'] < last['ema200'] and last['rsi'] > 30:
                    signal = "SELL"
        return signal
