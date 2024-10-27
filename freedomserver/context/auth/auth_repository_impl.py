from freedomserver.context.auth.auth_repository import AuthRepository
from freedomserver.context.auth.error.challenge_not_expired_error import ChallengeNotExpiredError
from freedomserver.context.auth.error.token_not_found_error import TokenNotFoundError
from redis import Redis

class AuthRepositoryImpl(AuthRepository):
    
    AUTH_DIRECTORY: str = "auth"
    CHALLENGE_EXPIRATION_TIME: int = 300
    AUTH_TOKEN_EXPIRATION_TIME: int = 3600

    def __init__(self, redis_connection: Redis):
        self._redis_connection = redis_connection

    def store_challenge(self, aci: str, device_id: str, challenge: str) -> None:
        self._redis_connection.setex(
            f"{self.AUTH_DIRECTORY}:{aci}:{device_id}",
            time=self.CHALLENGE_EXPIRATION_TIME,
            value=challenge)

    def get_challenge(self, aci: str, device_id: str) -> str:
        challenge: bytes = self._redis_connection.get(f"{self.AUTH_DIRECTORY}:{aci}:{device_id}")
        if challenge is None:
            raise ChallengeNotExpiredError("Challenge not found")
        return challenge.decode("utf-8")

    def delete_challenge(self, aci: str, device_id: str) -> None:
        self._redis_connection.delete(f"{self.AUTH_DIRECTORY}:{aci}:{device_id}")

    def store_token(self, aci: str, device_id: str, token: str) -> None:
        self._redis_connection.setex(
            f"{self.AUTH_DIRECTORY}:{aci}:{device_id}",
            time=self.AUTH_TOKEN_EXPIRATION_TIME,
            value=token)

    def get_token(self, aci: str, device_id: str) -> str:
        token: bytes = self._redis_connection.get(f"{self.AUTH_DIRECTORY}:{aci}:{device_id}")
        
        if token:
            return token.decode("utf-8")
        
        raise TokenNotFoundError("Token not found")

    def delete_token(self, aci: str, device_id: str) -> None:
        self._redis_connection.delete(f"{self.AUTH_DIRECTORY}:{aci}:{device_id}")