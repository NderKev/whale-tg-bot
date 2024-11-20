import requests
from app.config import BLOCKCHAIN_API_KEY, BLOCKCHAIN_API_URL, MIN_TRANSACTION_VALUE, ETHERSCAN_API_KEY

def fetch_large_transactions():
    """Fetch large transactions either from Whale Alert or Etherscan depending on configuration."""
    # Choose which API to use (Whale Alert or Etherscan)
    if BLOCKCHAIN_API_URL.lower() == "whale_alert":
        return fetch_whale_alert_transactions()
    elif BLOCKCHAIN_API_URL.lower() == "etherscan":
        return fetch_etherscan_transactions()
    else:
        print("Error: Unsupported blockchain API URL configuration.")
        return []

def fetch_whale_alert_transactions():
    """Fetch transactions from Whale Alert API."""
    params = {
        "api_key": BLOCKCHAIN_API_KEY,
        "min_value": MIN_TRANSACTION_VALUE  # Threshold in USD or equivalent
    }
    response = requests.get(BLOCKCHAIN_API_URL, params=params)
    if response.status_code == 200:
        return response.json().get("transactions", [])
    else:
        print(f"Error fetching Whale Alert transactions: {response.status_code} - {response.text}")
        return []

def fetch_etherscan_transactions():
    """Fetch large Ethereum transactions from Etherscan API."""
    url = f"https://api.etherscan.io/api"
    params = {
        "module": "account",
        "action": "tokentx",  # Using tokentx to track token transfers
        "address": "0xYourEthereumAddress",  # Replace with relevant Ethereum address (could be a whale address)
        "startblock": 0,  # Start from the first block
        "endblock": 99999999,  # Until the latest block
        "page": 1,  # Pagination
        "offset": 100,  # Number of results per page
        "sort": "desc",  # Sort by latest transactions
        "apikey": ETHERSCAN_API_KEY  # Etherscan API Key
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        transactions = response.json().get("result", [])
        # Filter out transactions based on MIN_TRANSACTION_VALUE (value threshold)
        large_transactions = [
            tx for tx in transactions if float(tx["value"]) / (10**18) >= MIN_TRANSACTION_VALUE
        ]
        return large_transactions
    else:
        print(f"Error fetching Etherscan transactions: {response.status_code} - {response.text}")
        return []

