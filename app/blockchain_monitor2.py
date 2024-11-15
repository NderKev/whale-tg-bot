# blockchain_monitor.py
import requests
from app.config import BLOCKCHAIN_API_KEY, BLOCKCHAIN_API_URL, MIN_TRANSACTION_VALUE

def fetch_large_transactions():
    """Fetch transactions above the threshold from the blockchain API."""
    params = {
        "api_key": BLOCKCHAIN_API_KEY,
        "min_value": MIN_TRANSACTION_VALUE
    }
    response = requests.get(BLOCKCHAIN_API_URL, params=params)
    if response.status_code == 200:
        return response.json().get("transactions", [])
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return []
