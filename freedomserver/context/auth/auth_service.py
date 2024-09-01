from freedomserver.context.auth.auth_repository import AuthRepository

class AuthService:
    
    def __init__(self, auth_repository: AuthRepository):
        self._auth_repository: AuthRepository = auth_repository

    def register_device(self, public_key: str, device_id: str) -> str:
        return self._auth_repository.register_device(public_key, device_id)

    def store_challenge(self, account_id: str, device_id: str, challenge: str) -> None:
        self._auth_repository.store_challenge(account_id, device_id, challenge)