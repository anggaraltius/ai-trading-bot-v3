import logging
from telegram_bot import TelegramBot

def main():
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler("logs/bot.log"),
            logging.StreamHandler()
        ]
    )

    logging.info("AI Trading Bot V3 starting...")

    bot = TelegramBot()
    bot.start()

if __name__ == "__main__":
    main()
