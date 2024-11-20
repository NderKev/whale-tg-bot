import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def send_alert(address, transaction):
    """
    Handle large transaction alert.
    """
    logger.info(f"🚨 Large Transaction Alert 🚨")
    logger.info(f"Watched Address: {address}")
    logger.info(f"Tx Hash: {transaction['hash']}")
    logger.info(f"From: {transaction['from']}")
    logger.info(f"To: {transaction['to']}")
    logger.info(f"Value: {transaction['value']} ETH")
    logger.info(f"Timestamp: {transaction['timestamp']}")
