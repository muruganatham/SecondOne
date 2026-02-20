"""
Rate Limiting & Request Throttling
Prevents API abuse and ensures fair resource usage
"""

from datetime import datetime, timedelta
from typing import Dict, Tuple
from functools import lru_cache
import time


class RateLimiter:
    """
    Simple in-memory rate limiter using sliding window
    For production, consider using Redis instead
    """

    def __init__(self, requests_per_minute: int = 60):
        self.requests_per_minute = requests_per_minute
        self.window = 60  # seconds
        self.requests: Dict[str, list] = {}

    def is_allowed(self, identifier: str) -> Tuple[bool, Dict]:
        """
        Check if a request from identifier is allowed
        Returns: (allowed: bool, info: dict with remaining/reset_time)
        """
        now = time.time()

        # Initialize if new identifier
        if identifier not in self.requests:
            self.requests[identifier] = []

        # Remove old requests outside the window
        self.requests[identifier] = [
            req_time
            for req_time in self.requests[identifier]
            if now - req_time < self.window
        ]

        # Check if limit exceeded
        if len(self.requests[identifier]) >= self.requests_per_minute:
            oldest_request = self.requests[identifier][0]
            reset_time = oldest_request + self.window
            remaining_wait = reset_time - now
            return False, {
                "limit": self.requests_per_minute,
                "remaining": 0,
                "reset_in_seconds": max(0, int(remaining_wait) + 1),
                "retry_after": int(remaining_wait) + 1,
            }

        # Allow and record request
        self.requests[identifier].append(now)
        return True, {
            "limit": self.requests_per_minute,
            "remaining": self.requests_per_minute - len(self.requests[identifier]),
            "reset_in_seconds": self.window,
        }

    def cleanup(self):
        """Remove old entries to prevent memory leak"""
        now = time.time()
        expired_keys = []

        for identifier, timestamps in self.requests.items():
            # Keep only recent timestamps
            self.requests[identifier] = [
                t for t in timestamps if now - t < self.window * 2
            ]
            # Remove completely empty entries
            if not self.requests[identifier]:
                expired_keys.append(identifier)

        for key in expired_keys:
            del self.requests[key]


class QueryCache:
    """
    Simple in-memory cache for database query results
    Format: {query_hash: (result, timestamp, ttl)}
    For production, use Redis for distributed caching
    """

    def __init__(self, ttl_seconds: int = 300):  # 5 minutes default
        self.cache: Dict[str, Tuple] = {}
        self.ttl_seconds = ttl_seconds

    @staticmethod
    def _hash_query(sql: str, user_id: str = None) -> str:
        """Create cache key from SQL and user context"""
        import hashlib

        combined = f"{sql}:{user_id or 'anonymous'}"
        return hashlib.md5(combined.encode()).hexdigest()

    def get(self, sql: str, user_id: str = None) -> Dict | None:
        """Get cached result if exists and not expired"""
        key = self._hash_query(sql, user_id)

        if key in self.cache:
            result, timestamp, ttl = self.cache[key]
            if time.time() - timestamp < ttl:
                return result
            else:
                # Expired, remove it
                del self.cache[key]

        return None

    def set(self, sql: str, result: Dict, user_id: str = None, ttl: int = None):
        """Cache a query result"""
        key = self._hash_query(sql, user_id)
        self.cache[key] = (result, time.time(), ttl or self.ttl_seconds)

    def clear(self):
        """Clear all cache"""
        self.cache.clear()

    def cleanup(self):
        """Remove expired entries"""
        now = time.time()
        expired_keys = [
            key
            for key, (_, timestamp, ttl) in self.cache.items()
            if now - timestamp > ttl
        ]
        for key in expired_keys:
            del self.cache[key]

    def get_stats(self) -> Dict:
        """Get cache statistics"""
        return {
            "total_entries": len(self.cache),
            "size_approx_mb": sum(
                len(str(result)) for result, _, _ in self.cache.values()
            )
            / (1024 * 1024),
        }


# Global singletons
rate_limiter = RateLimiter(requests_per_minute=100)
query_cache = QueryCache(ttl_seconds=300)  # 5 minute cache
