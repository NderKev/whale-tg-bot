import asyncio
import aiohttp
from etherscan_client import EtherscanClient
from app.eth_watcher.watcher_alerts import send_alert
from utils import filter_large_transactions
from config import ETHERSCAN_API_KEY, WATCHER_CHECK_INTERVAL

class WhaleWatcher:
    def __init__(self, addresses, alert_threshold):
        self.addresses = addresses
        self.alert_threshold = alert_threshold
        self.last_seen_txs = {address: None for address in addresses}
        self.client = EtherscanClient(ETHERSCAN_API_KEY)

    async def monitor_address(self, session, address):
        try:
            transactions = await self.client.fetch_transactions(session, address)
            for tx in transactions:
                if tx['hash'] == self.last_seen_txs[address]:
                    break
                large_txs = filter_large_transactions([tx], self.alert_threshold)
                for large_tx in large_txs:
                    send_alert(address, large_tx)

            if transactions:
                self.last_seen_txs[address] = transactions[0]['hash']
        except Exception as e:
            print(f"Error monitoring {address}: {e}")

    async def run(self):
        async with aiohttp.ClientSession() as session:
            while True:
                tasks = [self.monitor_address(session, address) for address in self.addresses]
                await asyncio.gather(*tasks)
                await asyncio.sleep(WATCHER_CHECK_INTERVAL)
