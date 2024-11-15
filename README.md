# **Crypto Whale Tracker Telegram Bot ( whale-tg-bot)** 

🐋 **Crypto Whale Tracker Telegram Bot** monitors large cryptocurrency transactions on the blockchain and alerts users when significant movements occur. This bot helps users stay informed about whale activities, which often signal market trends.

A telegram bot to track crypto whale activities in BTC, BNB, ETH, and other EVM-L1 and L2 networks.

---

## **Features**
- **Whale Activity Monitoring**: Tracks large crypto transactions above a user-defined threshold.
- **Multi-Token Support**: Subscribe to alerts for specific cryptocurrencies (e.g., BTC, ETH, USDT).
- **Real-Time Alerts**: Receive instant notifications on Telegram when whale transactions occur.
- **User-Friendly Commands**:
  - `/start`: Start using the bot.
  - `/subscribe [tokens]`: Subscribe to specific tokens (e.g., `/subscribe BTC ETH`).
- **Transaction History**: Logs all detected whale transactions for future analysis.

---

## **Architecture**
The bot comprises the following components:
1. **Blockchain Monitoring**:
   - Fetches transaction data from a blockchain monitoring API (e.g., Whale Alert API).
   - Filters transactions based on user-defined thresholds.
2. **Telegram Bot**:
   - Integrates with Telegram to handle user interactions and send alerts.
3. **Database**:
   - Stores user subscriptions and transaction logs using an SQLite database (or an alternative database service).

---

## **Tech Stack**
- **Python**: Main programming language.
- **Telegram Bot API**: Handles bot communication.
- **SQLAlchemy**: Database ORM for managing user subscriptions and logs.
- **Blockchain Monitoring API**: Fetches transaction data.
- **Requests**: HTTP library for API calls.

---

## **Setup Instructions**

### **Prerequisites**
- Python 3.8 or higher installed on your system.
- An API key from a blockchain monitoring service (e.g., Whale Alert, Etherscan).
- A Telegram bot token from [BotFather](https://t.me/botfather).
- (Optional) Docker for containerized deployment.

---

### **Installation**

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/NderKev/whale-tg-bot.git
   cd https://github.com/NderKev/whale-tg-bot
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Environment Variables**:
   Create a `.env` file or set these variables in your environment:
   ```env
   BLOCKCHAIN_API_KEY=your-blockchain-api-key
   TELEGRAM_BOT_TOKEN=your-telegram-bot-token
   DATABASE_URL=sqlite:///whale_tracker.db
   ```

4. **Run Database Migrations**:
   ```bash
   python -c "from app.database import Base, engine; Base.metadata.create_all(engine)"
   ```

5. **Start the Bot**:
   ```bash
   python main.py
   ```

---

### **Usage**
1. **Start the Bot**:  
   Message `/start` to the bot to initialize your account.
   
2. **Subscribe to Tokens**:  
   Use `/subscribe [tokens]` to start receiving alerts for specific cryptocurrencies. For example:
   ```plaintext
   /subscribe BTC ETH USDT
   ```

3. **Receive Alerts**:  
   Get real-time notifications about whale transactions directly in your Telegram chat.

---

## **Project Structure**
```plaintext
whale-tracker-bot/
├── app/
│   ├── __init__.py           # Package initialization
│   ├── config.py             # Configuration constants
│   ├── blockchain_monitor.py # Blockchain monitoring logic
│   ├── telegram_bot.py       # Telegram bot functionality
│   ├── database.py           # Database models and connection
│   ├── alerts.py             # Notification handler
├── requirements.txt          # Python dependencies
├── main.py                   # Main entry point
├── README.md                 # Project documentation
```

---

## **API Integration**
The bot fetches data from a blockchain monitoring API. Below are steps to configure the API:

1. **Whale Alert API**:
   - Sign up at [Whale Alert](https://www.whale-alert.io/).
   - Obtain your API key.
   - Set the `BLOCKCHAIN_API_KEY` environment variable.

2. **Etherscan API** (Ethereum-specific):
   - Sign up at [Etherscan](https://etherscan.io/).
   - Obtain your API key.
   - Adjust API calls in `blockchain_monitor.py`.

---

## **Future Enhancements**
- **Multi-Chain Support**: Add support for blockchains like Solana, Cardano, and Polygon.
- **Premium Features**:
  - Advanced filters (e.g., specific wallet addresses).
  - Whale behavior analytics.
- **Analytics Dashboard**: Visualize whale activity trends over time.
- **Docker Support**: Simplify deployment with a pre-configured Dockerfile.

---

## **Contributing**
Contributions are welcome! Follow these steps to contribute:
1. Fork the repository.
2. Create a feature branch:  
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes:  
   ```bash
   git commit -m "Add feature-name"
   ```
4. Push to the branch:  
   ```bash
   git push origin feature-name
   ```
5. Open a pull request.

---

## **License**
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## **Support**
For issues or questions, please reach out via:
- **Telegram**: [Your Telegram Link](https://t.me/yourusername)
- **Email**: your.email@example.com

---

## **Acknowledgments**
Special thanks to:
- [Whale Alert](https://www.whale-alert.io/) for their API.
- [Telegram](https://core.telegram.org/bots) for providing an excellent bot API.
- The Python community for the tools and libraries that power this project.

---
