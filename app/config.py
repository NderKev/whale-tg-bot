import os
from dotenv import load_dotenv

load_dotenv()

# Now you can access the environment variables
BLOCKCHAIN_API_KEY = os.getenv("BLOCKCHAIN_API_KEY")
BLOCKCHAIN_API_URL = "https://api.whale-alert.io/v1/transactions"
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///whale_tracker.db")
MIN_TRANSACTION_VALUE = int(os.getenv("MIN_TRANSACTION_VALUE", "1000"))
ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY")
WATCHER_CHECK_INTERVAL = os.getenv("WATCHER_CHECK_INTERVAL", "60")        