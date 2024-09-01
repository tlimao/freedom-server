from freedomserver.context.auth.auth_repository import AuthRepository
from redis import Redis

class AuthRepositoryImpl(AuthRepository):
    
    AUTH_DIRECTORY: str = "chat:auth"
    
    def __init__(self, redis_connection: Redis):
        self._redis_connection = redis_connection

    def register_device(self, public_key: str, device_id: str) -> str:
        return self._redis_connection.setex(f"{self.AUTH_DIRECTORY}:{public_key}", device_id)

    def store_challenge(self, account_id: str, device_id: str, challenge: str) -> None:
        self._redis_connection.store_challenge(account_id, device_id, challenge)