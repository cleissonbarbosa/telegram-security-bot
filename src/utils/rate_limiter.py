import time
from collections import deque
from datetime import datetime, timedelta
import asyncio


class RateLimiter:
    def __init__(self, max_requests, time_window):
        self.max_requests = max_requests
        self.time_window = time_window  # in seconds
        self.requests = deque()

    def can_make_request(self):
        now = datetime.now()

        # Remove old requests
        while self.requests and self.requests[0] < now - timedelta(
            seconds=self.time_window
        ):
            self.requests.popleft()

        # Check if we can make a new request
        if len(self.requests) < self.max_requests:
            self.requests.append(now)
            return True

        return False

    async def wait_if_needed(self):
        while not self.can_make_request():
            await asyncio.sleep(1)
        return True
