import requests


async def recent_vulnerabilities() -> str:
    """
    Fetches the most recent vulnerabilities from the CVE API.

    This asynchronous function makes a GET request to the CVE API to retrieve the 
    most recent vulnerabilities. It processes the response to extract and format 
    the top 5 vulnerabilities into a readable string.

    Returns:
        str: A formatted string containing the top 5 most recent vulnerabilities 
        with their IDs and summaries. If the request fails or an error occurs, 
        an appropriate error message is returned.
    """
    try:
        response = requests.get("https://cve.circl.lu/api/last")
        if response.status_code == 200:
            data = response.json()[:5]  # Get the top 5 most recent vulnerabilities
            mensagens = [f"{vuln['id']}: {vuln['summary']}" for vuln in data]
            return "\n\n".join(mensagens)
        else:
            return "❌ It was not possible to fetch the recent vulnerabilities. 😕"
    except Exception as e:
        return f"❌ Error scanning for vulnerabilities: {str(e)}"
