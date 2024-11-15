import os
from dotenv import load_dotenv

load_dotenv()

# Now you can access the environment variables
BLOCKCHAIN_API_KEY = os.getenv("BLOCKCHAIN_API_KEY")
BLOCKCHAIN_API_URL = "https://api.whale-alert.io/v1/transactions"
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///whale_tracker.db")
MIN_TRANSACTION_VALUE = int(os.getenv("MIN_TRANSACTION_VALUE", "1000000"))