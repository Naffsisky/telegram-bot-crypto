import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
COINMARKETCAP_API_KEY = os.getenv("COINMARKETCAP_API_KEY")

# File database
DB_FILE = "crypto_bot.db"
