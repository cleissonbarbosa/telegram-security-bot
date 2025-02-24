import logging
import time
from functools import wraps

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from telegram.constants import ParseMode
from googletrans import Translator

from config import SUPPORTED_LANGUAGES
from utils.metrics import metrics
from utils.rate_limiter import RateLimiter
from commands.handlers import (
    search_exploit,
    recent_vulnerabilities,
    get_vulnerability_stats,
    search_vulnerabilities,
)

# Initialize rate limiter
rate_limiter = RateLimiter(max_requests=30, time_window=60)


def measure_time(f):
    @wraps(f)
    async def wrapper(*args, **kwargs):
        start = time.time()
        try:
            result = await f(*args, **kwargs)
            metrics.log_command(f.__name__)
            return result
        finally:
            end = time.time()
            metrics.log_response_time(f.__name__, (end - start) * 1000)

    return wrapper


def validate_language(language: str) -> str:
    """Validate and normalize language code"""
    lang_code = language.lower()[:2]
    if lang_code not in SUPPORTED_LANGUAGES:
        return "en"
    return lang_code


@measure_time
async def exploit(update: Update, context: CallbackContext):
    """Enhanced exploit command with rate limiting and metrics"""
    if not await rate_limiter.wait_if_needed():
        await update.message.reply_text("⚠️ Too many requests. Please try again later.")
        return

    translator = Translator()
    language = "en"

    if context.args:
        if len(context.args) > 1:
            language = validate_language(context.args[1])
        vuln_id = context.args[0].upper()  # Normalize CVE ID

        try:
            result = await search_exploit(vuln_id, language)
            await update.message.reply_text(result, parse_mode=ParseMode.HTML)
        except Exception as e:
            metrics.log_error(str(e))
            error_msg = f"Error searching exploit: {str(e)}"
            if language != "en":
                error_msg = translator.translate(error_msg, dest=language).text
            await update.message.reply_text(f"❌ {error_msg}")
    else:
        await update.message.reply_text(
            "❌ Please provide a vulnerability ID (eg: /exploit CVE-2021-34527)"
        )


@measure_time
async def stats(update: Update, context: CallbackContext):
    """Enhanced stats command with bot metrics"""
    if not await rate_limiter.wait_if_needed():
        await update.message.reply_text("⚠️ Too many requests. Please try again later.")
        return

    # Add bot metrics to the stats
    if context.args and context.args[0] == "bot":
        bot_stats = metrics.get_stats()
        stats_text = (
            "🤖 <b>Bot Statistics</b>\n\n"
            f"Commands Used: {dict(bot_stats['commands'])}\n"
            f"API Calls: {dict(bot_stats['api_calls'])}\n"
            f"Errors: {dict(bot_stats['errors'])}\n"
            f"Avg Response Times: {dict(bot_stats['avg_response_times'])}ms"
        )
        await update.message.reply_text(stats_text, parse_mode=ParseMode.HTML)
        return

    # Regular vulnerability stats
    try:
        days = 7
        language = "en"

        if context.args:
            if len(context.args) >= 1:
                days = int(context.args[0])
            if len(context.args) >= 2:
                language = validate_language(context.args[1])

        result = await get_vulnerability_stats(days, language)
        await update.message.reply_text(result, parse_mode=ParseMode.HTML)

    except Exception as e:
        metrics.log_error(str(e))
        await update.message.reply_text(f"❌ Error getting statistics: {str(e)}")


@measure_time
async def search(update: Update, context: CallbackContext):
    """Handle the /search command to search vulnerabilities by keywords"""
    if not await rate_limiter.wait_if_needed():
        await update.message.reply_text("⚠️ Too many requests. Please try again later.")
        return

    translator = Translator()
    language = "en"
    page = 1

    if not context.args:
        await update.message.reply_text(
            "❌ Please provide search terms (eg: /search windows rce)"
        )
        return

    # Last argument might be language code
    if len(context.args) > 1 and context.args[-1].lower() in SUPPORTED_LANGUAGES:
        language = validate_language(context.args[-1])
        search_terms = " ".join(context.args[:-1])
    else:
        search_terms = " ".join(context.args)

    logging.info(
        f"Searching vulnerabilities with terms: {search_terms}, language: {language}"
    )

    searching_msg = f"🔍 Searching vulnerabilities matching: {search_terms}"
    if language != "en":
        searching_msg = translator.translate(searching_msg, dest=language).text
    await update.message.reply_text(searching_msg)

    try:
        result = await search_vulnerabilities(search_terms, language, page)

        # Add navigation buttons
        keyboard = [
            [
                InlineKeyboardButton(
                    "⬅️ Previous",
                    callback_data=f"search_{page-1}_{language}_{search_terms}",
                ),
                InlineKeyboardButton(
                    "Next ➡️", callback_data=f"search_{page+1}_{language}_{search_terms}"
                ),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            result, parse_mode=ParseMode.HTML, reply_markup=reply_markup
        )
    except Exception as e:
        metrics.log_error(str(e))
        error_msg = f"Error searching vulnerabilities: {str(e)}"
        if language != "en":
            error_msg = translator.translate(error_msg, dest=language).text
        await update.message.reply_text(f"❌ {error_msg}")


# Update help message
async def start(update: Update, context: CallbackContext):
    """Enhanced start command with more information"""
    help_text = (
        "🤖 <b>Security Vulnerability Bot</b>\n\n"
        "Available commands:\n"
        "/exploit <b>(CVE-ID)</b> [language] - Search for vulnerability details\n"
        "/search <i>(keywords)</i> [language] - Search vulnerabilities by keywords\n"
        "/recent [language] [page] - List recent vulnerabilities\n"
        "/stats [days] [language] - View vulnerability statistics\n"
        "/stats bot - View bot usage statistics\n\n"
        "Supported languages: " + ", ".join(SUPPORTED_LANGUAGES.keys()) + "\n\n"
        "Examples:\n"
        "/exploit CVE-2021-34527 pt\n"
        "/search windows rce es\n"
        "/recent fr 2\n"
        "/stats 30 de"
    )

    await update.message.reply_text(help_text, parse_mode=ParseMode.HTML)


async def recent_vuln(update: Update, context: CallbackContext) -> None:
    """
    Handle the /recent command to fetch and send recent vulnerabilities.

    Usage:
        /recent [language] [page]

    Example:
        /recent en 2
        /recent pt_br 1
    """
    translator = Translator()
    language = "en"
    page = 1

    if context.args:
        if len(context.args) >= 1:
            language = context.args[0]
        if len(context.args) >= 2:
            try:
                page = int(context.args[1])
                if page < 1:
                    page = 1
            except ValueError:
                await update.message.reply_text("Invalid page number. Using page 1.")
                page = 1

    logging.info(f"Received /recent_vuln command. Language: {language}, Page: {page}")

    fetching_msg = "Fetching recent vulnerabilities"
    if language != "en":
        translated_fetching_msg = translator.translate(fetching_msg, dest=language).text
        await update.message.reply_text(f"🔍 {translated_fetching_msg} ...")
    else:
        await update.message.reply_text(f"🔍 {fetching_msg} ...")

    result = await recent_vulnerabilities(language, page)

    # Add navigation buttons
    keyboard = [
        [
            InlineKeyboardButton(
                "⬅️ Previous", callback_data=f"page_{page-1}_{language}"
            ),
            InlineKeyboardButton("Next ➡️", callback_data=f"page_{page+1}_{language}"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        result, parse_mode=ParseMode.HTML, reply_markup=reply_markup
    )


async def handle_pagination(update: Update, context: CallbackContext) -> None:
    """
    Handle pagination callback queries from the inline keyboard buttons.

    The callback_data formats:
    - Recent: "page_<number>_<language>"
    - Search: "search_<number>_<language>_<query>"
    """
    query = update.callback_query
    await query.answer()  # Answer the callback query to remove the loading state

    try:
        # Parse the callback data
        parts = query.data.split("_")
        action = parts[0]
        page = int(parts[1])
        language = parts[2]

        # Don't allow negative pages
        if page < 1:
            await query.message.reply_text("You're already on the first page!")
            return

        if action == "page":
            # Handle recent vulnerabilities pagination
            result = await recent_vulnerabilities(language, page)
            keyboard = [
                [
                    InlineKeyboardButton(
                        "⬅️ Previous", callback_data=f"page_{page-1}_{language}"
                    ),
                    InlineKeyboardButton(
                        "Next ➡️", callback_data=f"page_{page+1}_{language}"
                    ),
                ]
            ]
        elif action == "search":
            # Handle search results pagination
            search_query = "_".join(parts[3:])  # Reconstruct search query
            result = await search_vulnerabilities(search_query, language, page)
            keyboard = [
                [
                    InlineKeyboardButton(
                        "⬅️ Previous",
                        callback_data=f"search_{page-1}_{language}_{search_query}",
                    ),
                    InlineKeyboardButton(
                        "Next ➡️",
                        callback_data=f"search_{page+1}_{language}_{search_query}",
                    ),
                ]
            ]
        else:
            await query.message.reply_text("❌ Invalid pagination action")
            return

        reply_markup = InlineKeyboardMarkup(keyboard)

        # Edit the message with new results and updated buttons
        await query.message.edit_text(
            result, reply_markup=reply_markup, parse_mode=ParseMode.HTML
        )

    except Exception as e:
        logging.error(f"Error handling pagination: {str(e)}")
        await query.message.reply_text(
            "❌ Error while changing page. Please try again."
        )
