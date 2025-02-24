import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Bot Configuration
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# API Configuration
NIST_API_KEY = os.getenv("NIST_API_KEY", "")  # Optional API key for higher rate limits
NIST_API_BASE_URL = "https://services.nvd.nist.gov/rest/json"

# Cache Configuration
CACHE_RECENT_VULNS = 300  # 5 minutes
CACHE_EXPLOIT = 3600  # 1 hour
CACHE_STATS = 1800  # 30 minutes
CACHE_SEARCH = 600

# Pagination Configuration
DEFAULT_PAGE_SIZE = 5
MAX_PAGE_SIZE = 10

# Rate Limiting
MAX_REQUESTS_PER_MINUTE = 30

# Supported Languages
SUPPORTED_LANGUAGES = {
    "en": "English",
    "pt": "Portuguese",
    "pt_br": "Brazilian Portuguese",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "it": "Italian",
    "nl": "Dutch",
    "ru": "Russian",
    "zh": "Chinese",
    "ja": "Japanese",
    "ko": "Korean",
}
