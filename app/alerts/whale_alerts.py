from telegram import Bot
from app.config import TELEGRAM_BOT_TOKEN

bot = Bot(token=TELEGRAM_BOT_TOKEN)

def send_whale_alert(chat_id, transaction):
    """Send a whale alert to a Telegram user."""
    message = (
        f"🐋 Whale Alert:\n"
        f"{transaction['amount']} {transaction['symbol']} "
        f"(${transaction['amount_usd']})\n"
        f"From: {transaction['from']['owner']}\n"
        f"To: {transaction['to']['owner']}\n"
        f"Txn: {transaction['hash']}"
    )
    bot.send_message(chat_id=chat_id, text=message)
