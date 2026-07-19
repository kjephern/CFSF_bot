import logging
import os

from dotenv import load_dotenv

from Bot.bot import Bot
from logging_config import setup_logging

if __name__ == "__main__":
    load_dotenv()
    setup_logging()
    TOKEN = os.getenv("DISCORD_TOKEN")
    logging.info("啟動中...")
    bot = Bot()
    if TOKEN:
        bot.run(TOKEN, log_level=logging.WARN)
