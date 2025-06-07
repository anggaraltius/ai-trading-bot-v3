import pandas as pd

class PatternDetector:

    @staticmethod
    def detect_double_top(df: pd.DataFrame) -> bool:
        recent = df.tail(50)
        tops = recent['high'].nlargest(2)
        diff = abs(tops.iloc[0] - tops.iloc[1])
        avg_price = recent['close'].mean()
        return diff <= avg_price * 0.01

    @staticmethod
    def detect_double_bottom(df: pd.DataFrame) -> bool:
        recent = df.tail(50)
        bottoms = recent['low'].nsmallest(2)
        diff = abs(bottoms.iloc[0] - bottoms.iloc[1])
        avg_price = recent['close'].mean()
        return diff <= avg_price * 0.01

    @staticmethod
    def detect_head_and_shoulders(df: pd.DataFrame) -> bool:
        recent = df.tail(60)
        highs = recent['high'].nlargest(3).sort_values()
        if len(highs) < 3:
            return False
        left_shoulder, head, right_shoulder = highs.iloc[0], highs.iloc[2], highs.iloc[1]
        cond1 = head > left_shoulder
        cond2 = head > right_shoulder
        cond3 = abs(left_shoulder - right_shoulder) < head * 0.02
        return cond1 and cond2 and cond3

    @staticmethod
    def detect_symmetric_triangle(df: pd.DataFrame) -> bool:
        recent = df.tail(50)
        high_diff = recent['high'].max() - recent['high'].min()
        low_diff = recent['low'].max() - recent['low'].min()
        return (high_diff / recent['close'].mean() < 0.05 and low_diff / recent['close'].mean() < 0.05)

    @staticmethod
    def detect_patterns(df: pd.DataFrame) -> list:
        patterns = []
        if PatternDetector.detect_double_top(df):
            patterns.append("Double Top")
        if PatternDetector.detect_double_bottom(df):
            patterns.append("Double Bottom")
        if PatternDetector.detect_head_and_shoulders(df):
            patterns.append("Head & Shoulders")
        if PatternDetector.detect_symmetric_triangle(df):
            patterns.append("Symmetric Triangle")
        return patterns
