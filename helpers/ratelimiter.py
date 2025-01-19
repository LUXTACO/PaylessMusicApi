import time
import redis

class RateLimitService:
    def __init__(self, database: redis.Redis, max_requests: int, time_window: int):
        self.database = database
        self.max_requests = max_requests
        self.time_window = time_window
        
    def on_request(self, ip_address: str) -> bool:
        key = f"ratelimit:{ip_address}"
        current_requests = self.database.get(key)
        if current_requests is None:
            self.database.setex(key, self.time_window, 1)
            return True
        if int(current_requests) < self.max_requests:
            self.database.incr(key)
            return True
        return False
