"""Simple in-memory TTL Cache to avoid external dependencies like Redis."""
import time
import hashlib
from typing import Optional

class AsyncTTLCache:
    def __init__(self, ttl_seconds: int = 3600):
        self.ttl = ttl_seconds
        self._cache = {}

    def _hash_query(self, query: str) -> str:
        return hashlib.sha256(query.strip().lower().encode()).hexdigest()

    async def get(self, query: str) -> Optional[str]:
        key = self._hash_query(query)
        if key in self._cache:
            entry = self._cache[key]
            if time.time() < entry['expires_at']:
                return entry['response']
            else:
                del self._cache[key]
        return None

    async def set(self, query: str, response: str):
        key = self._hash_query(query)
        self._cache[key] = {
            'response': response,
            'expires_at': time.time() + self.ttl
        }

# Global instance for the app
query_cache = AsyncTTLCache(ttl_seconds=3600)
