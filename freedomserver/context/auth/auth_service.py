from freedomserver.context.auth.auth_repository import AuthRepository
from freedomlib.key.key_manager import KeyManager
from freedomlib.key.key import Key
from freedomserver.context.auth.error.challenge_signature_not_valid_error import ChallengeSignatureNotValidError
from freedomserver.context.auth.error.token_not_found_error import TokenNotFoundError
from cryptography.hazmat.primitives import serialization
import base64
import secrets

class AuthService:
    
    def __init__(self, auth_repository: AuthRepository, key_manager: KeyManager):
        self._auth_repository: AuthRepository = auth_repository
        self._key_manager: KeyManager = key_manager

    def register_device(self, account_id: str, public_key: str, device_id: str) -> str:
        return self._auth_repository.register_device(account_id, public_key, device_id)

    def store_challenge(self, account_id: str, device_id: str, challenge: str) -> None:
        self._auth_repository.store_challenge(account_id, device_id, challenge)

    def verify_challenge(self, account_id: str, device_id: str, signed_challenge: str) -> str:
        key: Key = self._key_manager.get_account_key(account_id)
        
        self._verify_challenge_signature(key, account_id, device_id, signed_challenge)
        
        token: str = secrets.token_urlsafe(32)
        self._auth_repository.store_token(account_id, device_id, token)
        
        return token
        
    def _verify_challenge_signature(self, key: Key, account_id: str, device_id: str, signed_challenge: str) -> bool:
        try:
            # Carregar a chave pública do formato PEM
            public_key = serialization.load_pem_public_key(key.pub_key.encode())
            
            # Decodificar o desafio assinado de base64
            signature = base64.b64decode(signed_challenge)
            
            # Obter o desafio original do repositório
            challenge = self._auth_repository.get_challenge(account_id, device_id)
            
            # Verificar a assinatura
            public_key.verify(signature, challenge.encode())
            return True
        except Exception as e:
            # Se a verificação falhar, lançar uma exceção personalizada
            raise ChallengeSignatureNotValidError("A assinatura do desafio não é válida") from e

    def verify_token(self, account_id: str, device_id: str, token: str) -> bool:
        stored_token: bytes = self._auth_repository.get_token(account_id, device_id)
        
        if stored_token:
            return stored_token.decode("utf-8") == token
        
        raise TokenNotFoundError("Token not found")
