import json
from freedomlib.key.key import Key
from freedomlib.key.key_repository import KeyRepository
from redis import Redis

class KeyRepositoryImpl(KeyRepository):
    
    KEY_DIRECTORY: str = "keys"
    
    def __init__(self, redis_connection: Redis) -> None:
        self._redis_connection: Redis = redis_connection
    
    def save(self, account_pub_key: Key) -> Key:
        key: str = f"{self.KEY_DIRECTORY}:{account_pub_key.aci}"
        return self._redis_connection.save(key, json.dumps(account_pub_key.to_dict()))

    def get(self, key_id: str) -> Key:
        key: str = f"{self.KEY_DIRECTORY}:{key_id}"
        key_data: str = self._redis_connection.get(key)
        
        if 