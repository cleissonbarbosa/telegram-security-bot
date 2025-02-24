import logging

from telegram.ext import Application, CommandHandler, CallbackQueryHandler

from commands.entry_points import start, exploit, recent_vuln, handle_pagination, stats

# Put your bot token here
TELEGRAM_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


def main():
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("exploit", exploit))
    application.add_handler(CommandHandler("recent", recent_vuln))
    application.add_handler(CommandHandler("stats", stats))
    
    # Callback query handler for pagination
    application.add_handler(CallbackQueryHandler(handle_pagination))

    # Start bot
    application.run_polling()


if __name__ == "__main__":
    main()
