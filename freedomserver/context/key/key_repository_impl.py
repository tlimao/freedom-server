import json
from freedomlib.key.key import Key
from freedomlib.key.key_repository import KeyRepository
from redis import Redis

class KeyRepositoryImpl(KeyRepository):
    
    KEY_DIRECTORY_ID: str = "key:id"
    KEY_DIRECTORY_ACI: str = "key:aci"
    
    def __init__(self, redis_connection: Redis) -> None:
        self._redis_connection: Redis = redis_connection

    def save(self, key: Key) -> Key:
        self._redis_connection.set(
            f"{self.KEY_DIRECTORY_ID}:{key.id}",
            json.dumps(key.to_dict())
        )
        
        self._redis_connection.set(
            f"{self.KEY_DIRECTORY_ACI}:{key.aci}",
            key.id
        )

        return key

    def get_key_by_aci(self, aci: str) -> Key | None:
        key_id_data: bytes = self._redis_connection.get(f"{self.KEY_DIRECTORY_ACI}:{aci}")
        
        if not key_id_data:
            return None
        
        key_data: bytes = self._redis_connection.get(f"{self.KEY_DIRECTORY_ID}:{key_id_data.decode()}")
        
        return Key(**json.loads(key_data))

    def get(self, key_id: str) -> Key:
        return super().get(key_id)

    def delete(self, key_id: str) -> None:
        self._redis_connection.delete(f"{self.KEY_DIRECTORY_ID}:{key_id}")

    def update(self, key: Key) -> Key:
        return super().update(key)
