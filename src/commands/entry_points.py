from telegram import Update
from telegram.ext import CallbackContext

from commands.handlers import search_exploit, recent_vulnerabilities


async def exploit(update: Update, context: CallbackContext):
    """
    Handles the /exploit command to search for an exploit based on a provided vulnerability ID.

    Args:
        update (Update): The update object that contains information about the incoming update.
        context (CallbackContext): The context object that contains information about the current context.

    Usage:
        /exploit <vulnerability_id>

    Example:
        /exploit CVE-2021-34527

    Behavior:
        - If a vulnerability ID is provided, it searches for the exploit and replies with the result.
        - If no vulnerability ID is provided, it prompts the user to provide one.
    """
    if context.args:
        await update.message.reply_text("🔍 Searching for exploit information...")
        vuln_id = context.args[0]
        resultado = await search_exploit(vuln_id)
        await update.message.reply_text(resultado)
    else:
        await update.message.reply_text(
            "❌ Please provide a vulnerability ID (ex: /exploit CVE-2021-34527)."
        )


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
    await update.message.reply_text(
        "Welcome to the Exploits and Security Notifications Bot!\n"
        "Use /exploit <CVE-ID> to search for a vulnerability.\n"
        "Use /recent to see recent vulnerabilities."
    )


async def recent_vuln(update: Update, _context: CallbackContext) -> None:
    """
    Handle the /recent_vuln command to fetch and send recent vulnerabilities.

    This function is an entry point for the /recent_vuln command in the Telegram bot.
    It retrieves recent vulnerabilities and sends the result as a reply to the user.

    Args:
        update (Update): The update object that contains information about the incoming update.
        _context (CallbackContext): The context object that contains information about the current context.

    Returns:
        None
    """
    await update.message.reply_text("🔍 Fetching recent vulnerabilities...")
    result = recent_vulnerabilities()
    await update.message.reply_text(result)
