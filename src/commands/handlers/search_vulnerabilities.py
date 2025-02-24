import logging
import requests
from datetime import datetime, timedelta
from googletrans import Translator
from utils.cache import search_cache
from config import NIST_API_BASE_URL, DEFAULT_PAGE_SIZE


async def search_vulnerabilities(
    query: str, language: str = "en", page: int = 1, per_page: int = DEFAULT_PAGE_SIZE
) -> str:
    """
    Search for vulnerabilities using keywords.

    Args:
        query (str): The search query
        language (str): The language to translate the response to
        page (int): The page number
        per_page (int): Number of items per page
    """
    translator = Translator()
    cache_key = f"search_{query}_{language}_{page}"

    # Check cache first
    cached_result = search_cache.get(cache_key)
    if cached_result:
        return cached_result

    try:
        # Calculate pagination
        start_index = (page - 1) * per_page

        # Make request to NIST API
        url = f"{NIST_API_BASE_URL}/cves/2.0"
        params = {
            "keywordSearch": query,
            "resultsPerPage": per_page,
            "startIndex": start_index,
        }

        logging.info(
            f"Searching vulnerabilities: {url}?{'&'.join([f'{k}={v}' for k,v in params.items()])}"
        )
        response = requests.get(url, params=params, timeout=30)

        if response.status_code == 200:
            data = response.json()
            total_results = data.get("totalResults", 0)
            vulnerabilities = data.get("vulnerabilities", [])

            if not vulnerabilities:
                return await handle_error(
                    f"No vulnerabilities found matching '{query}'", language
                )

            # Format messages
            mensagens = []
            for vuln in vulnerabilities:
                try:
                    cve_data = vuln.get("cve", {})
                    vuln_id = cve_data.get("id", "Unknown ID")
                    descriptions = cve_data.get("descriptions", [])

                    # Get English description
                    description = next(
                        (
                            desc.get("value", "No description available")
                            for desc in descriptions
                            if desc.get("lang") == "en"
                        ),
                        "No description available",
                    )

                    # Get CVSS score if available
                    metrics = cve_data.get("metrics", {})
                    cvss_v3 = metrics.get("cvssMetricV31", [{}])[0].get("cvssData", {})
                    severity = ""
                    if cvss_v3:
                        base_score = cvss_v3.get("baseScore", "")
                        severity_level = cvss_v3.get("baseSeverity", "")
                        severity = f"(CVSS: {base_score} - {severity_level})"

                    message = (
                        f"<b><a href='https://nvd.nist.gov/vuln/detail/{vuln_id}'>"
                        f"{vuln_id}</a></b> {severity}\n{description[:250]}..."
                    )
                    mensagens.append(message)

                except Exception as e:
                    logging.error(f"Error formatting vulnerability: {str(e)}")
                    continue

            if not mensagens:
                return await handle_error("No valid vulnerabilities found", language)

            # Add pagination info
            total_pages = (total_results + per_page - 1) // per_page
            pagination_info = (
                f"\n\nSearch results for '{query}'\n"
                f"Page {page}/{total_pages} • Total: {total_results} vulnerabilities"
            )
            result = "\n\n".join(mensagens) + pagination_info

            if language != "en":
                result = translator.translate(result, dest=language).text

            # Cache the result
            search_cache.set(cache_key, result)
            return result

        else:
            error_msg = (
                f"Failed to search vulnerabilities. Status code: {response.status_code}"
            )
            return await handle_error(error_msg, language)

    except requests.Timeout:
        error_msg = "Request timed out. Please try again."
        return await handle_error(error_msg, language)

    except Exception as e:
        error_msg = f"Error searching vulnerabilities: {str(e)}"
        return await handle_error(error_msg, language)


async def handle_error(error_msg: str, language: str) -> str:
    """Helper function to handle error messages with translation"""
    translator = Translator()
    if language != "en":
        error_msg = translator.translate(error_msg, dest=language).text
    return f"❌ {error_msg}"
