from telegram import Update
from telegram.ext import CallbackContext

from commands.handlers import search_exploit, recent_vulnerabilities


async def exploit(update: Update, context: CallbackContext):
    if context.args:
        vuln_id = context.args[0]
        resultado = await search_exploit(vuln_id)
        await update.message.reply_text(resultado)
    else:
        await update.message.reply_text(
            "Please provide a vulnerability ID (ex: /exploit CVE-2021-34527)."
        )


async def start(update: Update, _context: CallbackContext):
    await update.message.reply_text(
        "Welcome to the Exploits and Security Notifications Bot!\n"
        "Use /exploit <CVE-ID> to search for a vulnerability.\n"
        "Use /recent to see recent vulnerabilities."
    )


async def recent_vuln(update: Update, _context: CallbackContext) -> None:
    result = recent_vulnerabilities()
    await update.message.reply_text(result)
