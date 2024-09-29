import logging

import requests
from googletrans import Translator


async def recent_vulnerabilities(language: str = "en") -> str:
    """
    Fetches the most recent vulnerabilities from the CVE API.

    This asynchronous function makes a GET request to the CVE API to retrieve the
    most recent vulnerabilities. It processes the response to extract and format
    the top 5 vulnerabilities into a readable string.

    Args:
        language (str): The language to translate the response to (default is "en").

    Returns:
        str: A formatted string containing the top 5 most recent vulnerabilities
        with their IDs and summaries. If the request fails or an error occurs,
        an appropriate error message is returned.
    """
    translator = Translator()
    try:
        response = requests.get("https://cve.circl.lu/api/last")
        if response.status_code == 200:
            logging.info("Recent vulnerabilities fetched successfully.")
            data = response.json()[:5]  # Get the top 5 most recent vulnerabilities
            mensagens = [
                f"<b><a href='https://www.cve.org/CVERecord?id={vuln['id']}'>{vuln['id']}</a></b>: {vuln['summary'][:250]}..."
                for vuln in data
            ]
            result = "\n\n".join(mensagens)

            if language != "en":
                translated_result = translator.translate(result, dest=language).text

                return translated_result
            else:
                return result

        else:
            logging.error("Error fetching recent vulnerabilities.")
            error_msg = "It was not possible to fetch the recent vulnerabilities."

            if language != "en":
                translated_error_msg = translator.translate(
                    error_msg, dest=language
                ).text

                return f"❌ {translated_error_msg} 😕"
            else:
                return f"❌ {error_msg} 😕"
    except Exception as e:
        logging.error(f"Error fetching recent vulnerabilities: {str(e)}")
        error_msg = "Error scanning for vulnerabilities"

        if language != "en":
            translated_error_msg = translator.translate(error_msg, dest=language).text

            return f"❌ {translated_error_msg}: {str(e)}"
        else:
            return f"❌ {error_msg}: {str(e)}"
