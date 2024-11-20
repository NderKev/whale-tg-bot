def filter_large_transactions(transactions, threshold):
    """
    Filter transactions exceeding a specific ETH value.
    """
    large_transactions = []
    for tx in transactions:
        value_in_eth = int(tx['value']) / 10**18
        if value_in_eth >= threshold:
            large_transactions.append({
                "hash": tx['hash'],
                "from": tx['from'],
                "to": tx['to'],
                "value": value_in_eth,
                "timestamp": int(tx['timeStamp']),
            })
    return large_transactions
