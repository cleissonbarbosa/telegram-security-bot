import logging
import requests
from datetime import datetime, timedelta
from googletrans import Translator
from utils.cache import recent_vulns_cache

async def recent_vulnerabilities(language: str = "en", page: int = 1, per_page: int = 5) -> str:
    """
    Fetches the most recent vulnerabilities from the NIST NVD API.
    
    Args:
        language (str): The language to translate the response to (default is "en")
        page (int): The page number (default is 1)
        per_page (int): Number of items per page (default is 5)
    """
    translator = Translator()
    cache_key = f"recent_{language}_{page}"
    
    # Check cache first
    cached_result = recent_vulns_cache.get(cache_key)
    if cached_result:
        return cached_result

    try:
        # Calculate dates for last 15 days
        end_date = datetime.now()
        start_date = end_date - timedelta(days=15)
        
        # Calculate pagination
        start_index = (page - 1) * per_page

        # Make request to NIST API
        url = "https://services.nvd.nist.gov/rest/json/cves/2.0"
        params = {
            'pubStartDate': start_date.strftime("%Y-%m-%dT%H:%M:%S.000"),
            'pubEndDate': end_date.strftime("%Y-%m-%dT%H:%M:%S.000"),
            'resultsPerPage': per_page,
            'startIndex': start_index
        }
        
        response = requests.get(url, params=params, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            total_results = data.get('totalResults', 0)
            vulnerabilities = data.get('vulnerabilities', [])
            
            if not vulnerabilities:
                return await handle_error("No vulnerabilities found for this period", language)
            
            # Format messages
            mensagens = []
            for vuln in vulnerabilities:
                try:
                    cve_data = vuln.get('cve', {})
                    vuln_id = cve_data.get('id', 'Unknown ID')
                    descriptions = cve_data.get('descriptions', [])
                    
                    # Get English description
                    description = next(
                        (desc.get('value', 'No description available') 
                         for desc in descriptions 
                         if desc.get('lang') == 'en'),
                        'No description available'
                    )
                    
                    # Get CVSS score if available
                    metrics = cve_data.get('metrics', {})
                    cvss_v3 = metrics.get('cvssMetricV31', [{}])[0].get('cvssData', {})
                    severity = ''
                    if cvss_v3:
                        base_score = cvss_v3.get('baseScore', '')
                        severity = f"(CVSS: {base_score})"
                    
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
            pagination_info = f"\n\nPage {page}/{total_pages} • Total: {total_results} vulnerabilities"
            result = "\n\n".join(mensagens) + pagination_info

            if language != "en":
                result = translator.translate(result, dest=language).text

            # Cache the result
            recent_vulns_cache.set(cache_key, result)
            return result
            
        else:
            error_msg = f"Failed to fetch vulnerabilities. Status code: {response.status_code}"
            return await handle_error(error_msg, language)
            
    except requests.Timeout:
        error_msg = "Request timed out. Please try again."
        return await handle_error(error_msg, language)
        
    except Exception as e:
        error_msg = f"Error scanning for vulnerabilities: {str(e)}"
        return await handle_error(error_msg, language)

async def handle_error(error_msg: str, language: str) -> str:
    """Helper function to handle error messages with translation"""
    translator = Translator()
    if language != "en":
        error_msg = translator.translate(error_msg, dest=language).text
    return f"❌ {error_msg}"
