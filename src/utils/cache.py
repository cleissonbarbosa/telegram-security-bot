from datetime import datetime, timedelta
from config import CACHE_EXPLOIT, CACHE_RECENT_VULNS, CACHE_STATS, CACHE_SEARCH

class ExpiringCache:
    def __init__(self, expiration_time=300):  # 5 minutos default
        self.cache = {}
        self.expiration_time = expiration_time

    def get(self, key):
        if key in self.cache:
            value, timestamp = self.cache[key]
            if datetime.now() - timestamp < timedelta(seconds=self.expiration_time):
                return value
            del self.cache[key]
        return None

    def set(self, key, value):
        self.cache[key] = (value, datetime.now())

# Cache instances
recent_vulns_cache = ExpiringCache(CACHE_RECENT_VULNS)
exploit_cache = ExpiringCache(CACHE_EXPLOIT)
stats_cache = ExpiringCache(CACHE_STATS)
search_cache = ExpiringCache(CACHE_SEARCH)