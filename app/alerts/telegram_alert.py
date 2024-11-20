import requests

def send_telegram_alert(transaction, bot_token, chat_id):
    """
    Send an alert to Telegram for a large transaction.
    """
    message = (
        f"🚨 Large Transaction Alert 🚨\n"
        f"Watched Address: {transaction['address']}\n"
        f"Tx Hash: {transaction['hash']}\n"
        f"From: {transaction['from']}\n"
        f"To: {transaction['to']}\n"
        f"Value: {transaction['value']} ETH"
    )
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    params = {"chat_id": chat_id, "text": message}
    requests.get(url, params=params)
