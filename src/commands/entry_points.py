import logging

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from telegram.constants import ParseMode
from googletrans import Translator

from commands.handlers import search_exploit, recent_vulnerabilities, get_vulnerability_stats


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

        result = await search_exploit(vuln_id, language)
        logging.info(f"Search result: {result}")
        await update.message.reply_text(result, parse_mode=ParseMode.HTML)
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
        "Welcome to the Exploits and Security Notifications Bot!\n\n"
        "Use /exploit *<CVE-ID>* _<LANG>_ to search for a vulnerability.\n"
        "Use /recent _<LANG>_ _<PAGE>_ to see recent vulnerabilities.\n"
        "Use /stats _<DAYS>_ _<LANG>_ to view recent vulnerability statistics.",
        parse_mode=ParseMode.MARKDOWN
    )


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
            InlineKeyboardButton("⬅️ Previous", callback_data=f"page_{page-1}_{language}"),
            InlineKeyboardButton("Next ➡️", callback_data=f"page_{page+1}_{language}")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        result, 
        parse_mode=ParseMode.HTML,
        reply_markup=reply_markup
    )


async def handle_pagination(update: Update, context: CallbackContext) -> None:
    """
    Handle pagination callback queries from the inline keyboard buttons.
    
    The callback_data format is: "page_<number>_<language>"
    """
    query = update.callback_query
    await query.answer()  # Answer the callback query to remove the loading state
    
    try:
        # Parse the callback data
        _, page, language = query.data.split('_')
        page = int(page)
        
        # Don't allow negative pages
        if page < 1:
            await query.message.reply_text("You're already on the first page!")
            return
            
        # Get new results for the requested page
        result = await recent_vulnerabilities(language, page)
        
        # Update navigation buttons
        keyboard = [
            [
                InlineKeyboardButton("⬅️ Previous", callback_data=f"page_{page-1}_{language}"),
                InlineKeyboardButton("Next ➡️", callback_data=f"page_{page+1}_{language}")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        # Edit the message with new results and updated buttons
        await query.message.edit_text(
            result,
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML
        )
        
    except Exception as e:
        logging.error(f"Error handling pagination: {str(e)}")
        await query.message.reply_text("❌ Error while changing page. Please try again.")


async def stats(update: Update, context: CallbackContext) -> None:
    """
    Handle the /stats command to get vulnerability statistics.
    
    Usage:
        /stats [days] [language]
        
    Example:
        /stats 7 en    - Get stats for last 7 days in English
        /stats 30 pt   - Get stats for last 30 days in Portuguese
    """
    translator = Translator()
    language = "en"
    days = 7  # default to 7 days
    
    if context.args:
        if len(context.args) >= 1:
            try:
                days = int(context.args[0])
                if days < 1 or days > 120:  # NIST API limit is 120 days
                    await update.message.reply_text("Days must be between 1 and 120. Using default (7 days).")
                    days = 7
            except ValueError:
                await update.message.reply_text("Invalid number of days. Using default (7 days).")
        if len(context.args) >= 2:
            language = context.args[1]

    logging.info(f"Received /stats command. Days: {days}, Language: {language}")

    fetching_msg = "Analyzing vulnerability statistics"
    if language != "en":
        translated_msg = translator.translate(fetching_msg, dest=language).text
        await update.message.reply_text(f"📊 {translated_msg} ...")
    else:
        await update.message.reply_text(f"📊 {fetching_msg} ...")

    try:
        result = await get_vulnerability_stats(days=days, language=language)
        await update.message.reply_text(result, parse_mode=ParseMode.HTML)
    except Exception as e:
        error_msg = f"Error getting statistics: {str(e)}"
        if language != "en":
            error_msg = translator.translate(error_msg, dest=language).text
        await update.message.reply_text(f"❌ {error_msg}")
