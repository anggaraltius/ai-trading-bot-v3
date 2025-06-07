class RiskManagement:

    def __init__(self, account_balance: float, risk_per_trade: float = 0.02, sl_buffer: float = 0.01, rr_ratio: float = 2.0):
        """
        account_balance: total balance account (USDT)
        risk_per_trade: max loss per trade (% dari balance)
        sl_buffer: jarak stoploss dari entry (%)
        rr_ratio: risk reward ratio
        """
        self.balance = account_balance
        self.risk_pct = risk_per_trade
        self.sl_buffer = sl_buffer
        self.rr_ratio = rr_ratio

    def calculate_position_size(self, entry_price: float):
        dollar_risk = self.balance * self.risk_pct
        stop_loss_price = entry_price * (1 - self.sl_buffer)
        sl_distance = entry_price - stop_loss_price

        if sl_distance == 0:
            return 0, 0, 0, 0

        qty = dollar_risk / sl_distance
        take_profit_price = entry_price + (self.rr_ratio * sl_distance)
        stop_loss_price = round(stop_loss_price, 4)
        take_profit_price = round(take_profit_price, 4)
        qty = round(qty, 6)

        return qty, stop_loss_price, take_profit_price, dollar_risk

    def generate_trade_plan(self, entry_price: float):
        qty, sl, tp, dollar_risk = self.calculate_position_size(entry_price)
        plan = {
            "Entry Price": round(entry_price, 4),
            "Position Size": qty,
            "Stop Loss": sl,
            "Take Profit": tp,
            "Risk Amount (USD)": round(dollar_risk, 2)
        }
        return plan
