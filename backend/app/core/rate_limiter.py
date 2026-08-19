import time
from typing import Dict, List
import threading

class SlidingWindowRateLimiter:
    """
    Sliding window log rate limiter supporting high concurrency.
    Protects the AI endpoints and avoids DDoS / resource exhaustion.
    """
    def __init__(self, requests_per_minute: int = 120):
        self.rpm = requests_per_minute
        self.window = 60.0
        self._history: Dict[str, List[float]] = {}
        self._lock = threading.Lock()

    def is_allowed(self, client_id: str) -> bool:
        now = time.time()
        with self._lock:
            if client_id not in self._history:
                self._history[client_id] = [now]
                return True
            
            # Prune timestamps older than window
            cutoff = now - self.window
            valid_timestamps = [t for t in self._history[client_id] if t > cutoff]
            
            if len(valid_timestamps) >= self.rpm:
                self._history[client_id] = valid_timestamps
                return False
            
            valid_timestamps.append(now)
            self._history[client_id] = valid_timestamps
            return True

rate_limiter = SlidingWindowRateLimiter(requests_per_minute=300)
