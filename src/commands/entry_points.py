import logging

from telegram import Update
from telegram.ext import CallbackContext
from telegram.constants import ParseMode
from googletrans import Translator

from commands.handlers import search_exploit, recent_vulnerabilities


async def exploit(update: Update, context: CallbackContext):
    """
    Handles the /exploit command to search for an exploit based on a provided vulnerability ID.

    Args:
        update (Update): The update object that contains information about the incoming update.
        context (CallbackContext): The context object that contains information about the current context.

    Usage:
        /exploit <vulnerability_id>
        /exploit <vulnerability_id> <language>

    Example:
        /exploit CVE-2021-34527
        /exploit CVE-2021-34527 pt_br

    Behavior:
        - If a vulnerability ID is provided, it searches for the exploit and replies with the result.
        - If no vulnerability ID is provided, it prompts the user to provide one.
        - If a language is provided, it translates the message to that language.
        - If no language is provided, it defaults to English.
    """
    translator = Translator()
    if context.args:
        language = context.args[1] if len(context.args) > 1 else "en"
        vuln_id = context.args[0]
        logging.info(
            f"Searching for exploit information for {vuln_id}, language: {language}"
        )

        info = "Searching for exploit information"
        if language != "en":
            translated_info = translator.translate(info, dest=language).text
            await update.message.reply_text(f"🔍 {translated_info} ...")
        else:
            await update.message.reply_text(f"🔍 {info} ...")

        resultado = await search_exploit(vuln_id, language)
        logging.info(f"Search result: {resultado}")
        await update.message.reply_text(resultado, parse_mode=ParseMode.HTML)
    else:
        logging.warning("No vulnerability ID provided.")
        error_msg = "Please provide a vulnerability ID (eg: /exploit CVE-2021-34527)."
        if language != "en":
            translated_result = translator.translate(error_msg, dest=language).text
            await update.message.reply_text(f"❌ {translated_result}")
        else:
            await update.message.reply_text(f"❌ {error_msg}")


async def start(update: Update, _context: CallbackContext):
    """
    Handles the /start command for the Telegram bot.

    Sends a welcome message to the user with instructions on how to use the bot.

    Args:
        update (Update): The update object that contains information about the incoming update.
        _context (CallbackContext): The context object that contains information about the current context.

    Returns:
        None
    """
    logging.info("Received /start command.")

    await update.message.reply_text(
        "Welcome to the Exploits and Security Notifications Bot!\n"
        "Use /exploit <CVE-ID> to search for a vulnerability.\n"
        "Use /recent to see recent vulnerabilities."
    )


async def recent_vuln(update: Update, context: CallbackContext) -> None:
    """
    Handle the /recent command to fetch and send recent vulnerabilities.

    This function is an entry point for the /recent_vuln command in the Telegram bot.
    It retrieves recent vulnerabilities and sends the result as a reply to the user.

    Args:
        update (Update): The update object that contains information about the incoming update.
        _context (CallbackContext): The context object that contains information about the current context.

    Usage:
        /recent
        /recent <language>

    Returns:
        None

    Behavior:
        - If a language is provided, it translates the message to that language.
        - If no language is provided, it defaults to English.
    """
    translator = Translator()
    language = "en"
    if context.args:
        language = context.args[0] if len(context.args) >= 1 else "en"

    logging.info("Received /recent_vuln command.")

    fetching_msg = "Fetching recent vulnerabilities"
    if language != "en":
        translated_fetching_msg = translator.translate(fetching_msg, dest=language).text
        await update.message.reply_text(f"🔍 {translated_fetching_msg} ...")
    else:
        await update.message.reply_text(f"🔍 {fetching_msg} ...")

    result = await recent_vulnerabilities(language)

    logging.info(f"Recent vulnerabilities: {result}")
    await update.message.reply_text(result, parse_mode=ParseMode.HTML)
