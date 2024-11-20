import asyncio
import aiohttp
from config import ETHERSCAN_API_KEY

# Configuration
WATCH_ADDRESSES = [
    "0x95222290DD7278Aa3Ddd389Cc1E1d165CC4BAfe5",
]  # List of addresses to monitor
ALERT_THRESHOLD = 50  # Threshold in ETH to trigger an alert
CHECK_INTERVAL = 60  # Interval (in seconds) to check for new transactions

async def fetch_transactions(session, address, api_key, start_block=0, end_block=99999999):
    """
    Asynchronously fetch transactions from Etherscan for a specific Ethereum address.
    """
    url = "https://api.etherscan.io/api"
    params = {
        "module": "account",
        "action": "txlist",
        "address": address,
        "startblock": start_block,
        "endblock": end_block,
        "sort": "desc",  # Newest first
        "apikey": api_key
    }
    try:
        async with session.get(url, params=params) as response:
            data = await response.json()
            if data["status"] == "1":  # Success
                return data["result"]
            elif data["status"] == "0":  # Error
                print(f"Error for {address}: {data['message']}")
                return []
    except Exception as e:
        print(f"API Request failed for {address}: {e}")
        return []

def filter_large_transactions(transactions, threshold):
    """
    Filter transactions exceeding a specific ETH value.
    """
    large_transactions = []
    for tx in transactions:
        value_in_eth = int(tx['value']) / 10**18  # Convert Wei to ETH
        if value_in_eth >= threshold:
            large_transactions.append({
                "hash": tx['hash'],
                "from": tx['from'],
                "to": tx['to'],
                "value": value_in_eth,
                "timestamp": int(tx['timeStamp']),
            })
    return large_transactions

def alert_large_transaction(address, transaction):
    """
    Send an alert for a large transaction.
    """
    print(f"🚨 Large Transaction Alert 🚨")
    print(f"Watched Address: {address}")
    print(f"Tx Hash: {transaction['hash']}")
    print(f"From: {transaction['from']}")
    print(f"To: {transaction['to']}")
    print(f"Value: {transaction['value']} ETH")
    print(f"Timestamp: {transaction['timestamp']}")

async def monitor_address(session, address, last_seen_txs):
    """
    Monitor transactions for a single address.
    """
    transactions = await fetch_transactions(session, address, ETHERSCAN_API_KEY)
    if not transactions:
        print(f"No transactions found for {address} or API error. Retrying...")
        return

    # Process new transactions for the current address
    for tx in transactions:
        if tx['hash'] == last_seen_txs[address]:
            break  # Stop processing already seen transactions

        large_txs = filter_large_transactions([tx], ALERT_THRESHOLD)
        for large_tx in large_txs:
            alert_large_transaction(address, large_tx)

    # Update last seen transaction for this address
    last_seen_txs[address] = transactions[0]['hash'] if transactions else last_seen_txs[address]

async def whale_watch():
    """
    Main function to monitor whale transactions across multiple addresses concurrently.
    """
    last_seen_txs = {address: None for address in WATCH_ADDRESSES}  # Track last seen transaction hash for each address
    print(f"Starting Whale Watcher... Monitoring transactions over {ALERT_THRESHOLD} ETH for multiple addresses.")

    async with aiohttp.ClientSession() as session:
        while True:
            tasks = [monitor_address(session, address, last_seen_txs) for address in WATCH_ADDRESSES]
            await asyncio.gather(*tasks)  # Run all monitoring tasks concurrently
            await asyncio.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    asyncio.run(whale_watch())
