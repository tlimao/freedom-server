import json
from redis import Redis

from freedomlib.key.key_box import KeyBox
from freedomserver.context.key.repository.key_repository import KeyRepository

class KeyRepositoryImpl(KeyRepository):
    
    KEY_DIRECTORY_ID: str = "key:id"
    KEY_DIRECTORY_ACI: str = "key:aci"
    
    def __init__(self, redis_connection: Redis) -> None:
        self._redis_connection: Redis = redis_connection

    def save(self, key_box: KeyBox) -> KeyBox:
        self._redis_connection.set(
            f"{self.KEY_DIRECTORY_ID}:{key_box.id}",
            json.dumps(key_box.to_dict())
        )
        
        self._redis_connection.set(
            f"{self.KEY_DIRECTORY_ACI}:{key_box.aci}",
            key_box.id
        )

        return key_box

    def get_key_by_aci(self, aci: str) -> KeyBox | None:
        key_id_data: bytes = self._redis_connection.get(f"{self.KEY_DIRECTORY_ACI}:{aci}")
        
        if not key_id_data:
            return None
        
        key_data: bytes = self._redis_connection.get(f"{self.KEY_DIRECTORY_ID}:{key_id_data.decode()}")
        
        return KeyBox(**json.loads(key_data))

    def get(self, key_id: str) -> KeyBox:
        return super().get(key_id)

    def delete(self, key_id: str) -> None:
        self._redis_connection.delete(f"{self.KEY_DIRECTORY_ID}:{key_id}")

    def update(self, key: KeyBox) -> KeyBox:
        return super().update(key)
