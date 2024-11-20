import aiohttp

class EtherscanClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.etherscan.io/api"

    async def fetch_transactions(self, session, address, start_block=0, end_block=99999999):
        params = {
            "module": "account",
            "action": "txlist",
            "address": address,
            "startblock": start_block,
            "endblock": end_block,
            "sort": "desc",
            "apikey": self.api_key,
        }
        async with session.get(self.base_url, params=params) as response:
            data = await response.json()
            if data.get("status") == "1":
                return data.get("result", [])
            else:
                raise ValueError(f"Error fetching transactions for {address}: {data.get('message')}")
