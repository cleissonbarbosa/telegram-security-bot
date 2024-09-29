from telegram.ext import Application, CommandHandler

from commands.entry_points import start, exploit, recent_vuln

# Coloque o token do seu bot aqui
TELEGRAM_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"


def main():
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("exploit", exploit))
    application.add_handler(CommandHandler("recent", recent_vuln))

    # Iniciar o bot
    application.run_polling()


if __name__ == "__main__":
    main()
