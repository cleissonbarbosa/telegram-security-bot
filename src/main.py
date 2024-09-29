import logging

from telegram.ext import Application, CommandHandler

from commands.entry_points import start, exploit, recent_vuln

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

    # Start bot
    application.run_polling()


if __name__ == "__main__":
    main()
