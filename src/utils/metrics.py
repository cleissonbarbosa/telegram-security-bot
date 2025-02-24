import logging
from datetime import datetime
from collections import defaultdict


class BotMetrics:
    def __init__(self):
        self.command_usage = defaultdict(int)
        self.api_calls = defaultdict(int)
        self.errors = defaultdict(int)
        self.response_times = defaultdict(list)

    def log_command(self, command: str):
        self.command_usage[command] += 1

    def log_api_call(self, endpoint: str):
        self.api_calls[endpoint] += 1

    def log_error(self, error_type: str):
        self.errors[error_type] += 1

    def log_response_time(self, command: str, time_ms: float):
        self.response_times[command].append(time_ms)

    def get_stats(self):
        stats = {
            "commands": dict(self.command_usage),
            "api_calls": dict(self.api_calls),
            "errors": dict(self.errors),
            "avg_response_times": {
                cmd: sum(times) / len(times)
                for cmd, times in self.response_times.items()
            },
        }
        return stats


metrics = BotMetrics()
