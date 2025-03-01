import telegram
from telegram.ext import Updater, CommandHandler, CallbackContext
import yfinance as yf

# Replace with your bot token
TOKEN = "7632551956:AAF9czsBL5xgbRkrF-B28yNpHC8W7oZFwsk"

def stock(update: telegram.Update, context: CallbackContext) -> None:
    """Fetches stock price and sends it to the user."""
    try:
        if not context.args:
            update.message.reply_text("Please provide a stock symbol. Example: /stock AAPL")
            return

        symbol = context.args[0].upper()  # Get stock symbol from command arguments
        stock_data = yf.Ticker(symbol)

        # Extract stock data safely
        info = stock_data.info
        current_price = info.get('regularMarketPrice')
        change = info.get('regularMarketChange', 0)
        change_percent = info.get('regularMarketChangePercent', 0)

        if current_price is None:
            update.message.reply_text("Stock data not available. Please check the symbol.")
            return

        message = f"{symbol}: ${current_price:.2f} (Change: {change:.2f}, {change_percent:.2f}%)"
        update.message.reply_text(message)

    except Exception as e:
        update.message.reply_text(f"An error occurred: {e}")

def main() -> None:
    """Starts the Telegram bot."""
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Register command handler
    dispatcher.add_handler(CommandHandler("stock", stock))

    # Start polling for updates
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
