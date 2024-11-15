from telegram.ext import ApplicationBuilder, CommandHandler, CallbackContext
from telegram import Update
from app.database import SessionLocal, User
from app.config import TELEGRAM_BOT_TOKEN
from typing import List
import logging
import os

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def validate_tokens(tokens: str) -> tuple[bool, List[str]]:
    """
    Validate the token symbols.
    Returns (is_valid, cleaned_tokens).
    """
    if not tokens:
        return False, []
    
    cleaned_tokens = [t.strip().upper() for t in tokens.split() if t.strip()]
    # Add additional validation rules here (e.g., check against a list of valid tokens)
    return bool(cleaned_tokens), cleaned_tokens

async def start(update: Update, context: CallbackContext) -> None:
    """Welcome message and instructions."""
    try:
        chat_id = update.effective_chat.id
        with SessionLocal() as session:
            user = session.query(User).filter_by(chat_id=str(chat_id)).first()
            if not user:
                user = User(chat_id=str(chat_id), preferences="")
                session.add(user)
                session.commit()
                logger.info(f"New user registered: {chat_id}")
            
            await update.message.reply_text(
                "🐋 Welcome to Whale Tracker Bot!\n\n"
                "Commands:\n"
                "/subscribe [tokens] - Track specific cryptocurrencies\n"
                "/unsubscribe - Stop tracking all tokens\n"
                "/list - Show your current subscriptions\n"
                "/help - Show this help message"
            )
    except Exception as e:
        logger.error(f"Error in start command: {str(e)}")
        await update.message.reply_text(
            "Sorry, something went wrong. Please try again later."
        )

async def subscribe(update: Update, context: CallbackContext) -> None:
    """Subscribe to specific tokens."""
    try:
        chat_id = update.effective_chat.id
        tokens = " ".join(context.args)
        
        is_valid, cleaned_tokens = validate_tokens(tokens)
        if not is_valid:
            await update.message.reply_text(
                "⚠️ Please provide valid token symbols.\n"
                "Example: /subscribe BTC ETH"
            )
            return

        with SessionLocal() as session:
            user = session.query(User).filter_by(chat_id=str(chat_id)).first()
            if not user:
                await update.message.reply_text("Please /start the bot first!")
                return
            
            user.preferences = " ".join(cleaned_tokens)
            session.commit()
            logger.info(f"User {chat_id} subscribed to: {cleaned_tokens}")
            
            await update.message.reply_text(
                f"✅ You are now tracking whale movements for:\n"
                f"{', '.join(cleaned_tokens)}"
            )
    except Exception as e:
        logger.error(f"Error in subscribe command: {str(e)}")
        await update.message.reply_text(
            "Sorry, something went wrong. Please try again later."
        )

async def unsubscribe(update: Update, context: CallbackContext) -> None:
    """Unsubscribe from all tokens."""
    try:
        chat_id = update.effective_chat.id
        with SessionLocal() as session:
            user = session.query(User).filter_by(chat_id=str(chat_id)).first()
            if user:
                user.preferences = ""
                session.commit()
                logger.info(f"User {chat_id} unsubscribed from all tokens")
                await update.message.reply_text("You've unsubscribed from all tokens.")
            else:
                await update.message.reply_text("Please /start the bot first!")
    except Exception as e:
        logger.error(f"Error in unsubscribe command: {str(e)}")
        await update.message.reply_text(
            "Sorry, something went wrong. Please try again later."
        )

async def list_subscriptions(update: Update, context: CallbackContext) -> None:
    """List current token subscriptions."""
    try:
        chat_id = update.effective_chat.id
        with SessionLocal() as session:
            user = session.query(User).filter_by(chat_id=str(chat_id)).first()
            if not user or not user.preferences:
                await update.message.reply_text(
                    "You're not tracking any tokens.\n"
                    "Use /subscribe [tokens] to start tracking."
                )
                return
            
            tokens = user.preferences.split()
            await update.message.reply_text(
                "🔍 Your current subscriptions:\n"
                f"{', '.join(tokens)}"
            )
    except Exception as e:
        logger.error(f"Error in list command: {str(e)}")
        await update.message.reply_text(
            "Sorry, something went wrong. Please try again later."
        )

def setup_bot() -> None:
    """Set up Telegram bot handlers."""
    try:
        if not TELEGRAM_BOT_TOKEN:
            raise ValueError("Telegram bot token not configured")
        
        application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
        
        # Register command handlers
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("subscribe", subscribe))
        application.add_handler(CommandHandler("unsubscribe", unsubscribe))
        application.add_handler(CommandHandler("list", list_subscriptions))
        application.add_handler(CommandHandler("help", start))  # Help shows the same as start
        
        logger.info("Bot setup completed successfully")
        
        # Start webhook or polling based on environment
        if os.getenv('ENVIRONMENT') == 'production':
            port = int(os.getenv('PORT', 8443))
            app_name = os.getenv('APP_NAME')
            
            # Start webhook
            application.run_webhook(
                listen="0.0.0.0",
                port=port,
                url_path=TELEGRAM_BOT_TOKEN,
                webhook_url=f"https://{app_name}.herokuapp.com/{TELEGRAM_BOT_TOKEN}"
            )
            logger.info(f"Bot webhook started on port {port}")
        else:
            # Start polling for development
            application.run_polling()
            logger.info("Bot polling started")
            
    except ValueError as e:
        logger.error(f"Configuration error: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Failed to setup bot: {str(e)}")
        raise
