import json
from redis import Redis


class AccountCache:
    
    def __init__(self, redis_connection: Redis) -> None:
        self._redis_connection: Redis = redis_connection
    
    def set(self, key: str, value: dict, expiration: int = 10000) -> None:
        self._redis_connection.setex(key, expiration, value)

    def get(self, key: str) -> dict | None:
        data: bytes = self._redis_connection.get(key)
        
        if data:
            return json.loads(data)
        
        return None

    def delete(self, key: str) -> None:
        self._redis_connection.delete(key)