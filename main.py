import time
from app.blockchain_monitor import fetch_large_transactions
from app.alerts.whale_alerts import send_whale_alert
from app.telegram_bot import setup_bot
from app.database import SessionLocal, User, Transaction

def monitor_transactions():
    """Monitor and alert users about large transactions."""
    transactions = fetch_large_transactions()
    with SessionLocal() as session:
        for txn in transactions:
            if not session.query(Transaction).filter_by(tx_hash=txn['hash']).first():
                # Save transaction to avoid duplicate alerts
                session.add(Transaction(
                    tx_hash=txn["hash"],
                    symbol=txn["symbol"],
                    amount=txn["amount"],
                    amount_usd=txn["amount_usd"]
                ))
                session.commit()
                # Alert subscribed users
                for user in session.query(User).all():
                    preferences = user.preferences.split(",") if user.preferences else []
                    if not preferences or txn["symbol"] in preferences:
                        send_whale_alert(user.chat_id, txn)

if __name__ == "__main__":
    # Start the Telegram bot
    bot = setup_bot()
    bot.start_polling()

    # Start monitoring blockchain transactions
    while True:
        monitor_transactions()
        time.sleep(60)  # Fetch new data every minute
