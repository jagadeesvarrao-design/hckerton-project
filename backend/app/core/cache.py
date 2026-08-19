import time
from typing import Any, Optional, Dict
import threading

class MemoryCache:
    """
    Lock-free read, thread-safe write, high-throughput in-memory cache
    designed for 100,000+ simultaneous requests with zero disk IO.
    """
    def __init__(self, default_ttl: int = 3600):
        self._store: Dict[str, tuple[Any, float]] = {}
        self._lock = threading.Lock()
        self.default_ttl = default_ttl

    def get(self, key: str) -> Optional[Any]:
        item = self._store.get(key)
        if item is None:
            return None
        value, expiry = item
        if expiry > 0 and time.time() > expiry:
            # Expired, clean up asynchronously or on next write
            return None
        return value

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        ttl_val = ttl if ttl is not None else self.default_ttl
        expiry = time.time() + ttl_val if ttl_val > 0 else 0
        with self._lock:
            self._store[key] = (value, expiry)

    def delete(self, key: str) -> None:
        with self._lock:
            self._store.pop(key, None)

    def clear(self) -> None:
        with self._lock:
            self._store.clear()

    def size(self) -> int:
        return len(self._store)

# Global singleton cache instance
cache = MemoryCache()
