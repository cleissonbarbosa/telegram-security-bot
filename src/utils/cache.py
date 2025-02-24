from functools import lru_cache
from datetime import datetime, timedelta

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

# Cache para vulnerabilidades recentes
recent_vulns_cache = ExpiringCache(300)  # 5 minutos
exploit_cache = ExpiringCache(3600)  # 1 hora
stats_cache = ExpiringCache(1800)  # 30 minutos - adicionado para estatísticas 