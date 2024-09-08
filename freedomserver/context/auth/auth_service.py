from freedomserver.context.auth.auth_repository import AuthRepository
from freedomlib.key.key_manager import KeyManager
from freedomlib.key.key import Key
from freedomserver.context.auth.error.challenge_signature_not_valid_error import ChallengeSignatureNotValidError
from freedomserver.context.auth.error.token_not_found_error import TokenNotFoundError
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ed25519
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

    def verify_challenge(self, account_id: str, device_id: str, signed_challenge: str, client_pub_key: str) -> str:
        self._verify_challenge_signature(client_pub_key, account_id, device_id, signed_challenge)
        
        token: str = secrets.token_urlsafe(32)
        self._auth_repository.store_token(account_id, device_id, token)
        
        return token
        
    def _verify_challenge_signature(self, key: str, account_id: str, device_id: str, signed_challenge: str) -> bool:
        try:
            # Decodificar a chave pública de base64
            public_key_bytes = base64.b64decode(key)
            
            # Reconstruir a chave pública Ed25519
            public_key = ed25519.Ed25519PublicKey.from_public_bytes(public_key_bytes)
            
            # Decodificar o desafio assinado de base64
            signature = base64.b64decode(signed_challenge.encode())
            
            # Obter o desafio original do repositório
            challenge = self._auth_repository.get_challenge(account_id, device_id)
            
            # Verificar a assinatura
            public_key.verify(signature, base64.b64decode(challenge))
            return True
        except Exception as e:
            # Se a verificação falhar, lançar uma exceção personalizada
            raise ChallengeSignatureNotValidError("A assinatura do desafio não é válida") from e

    def verify_token(self, account_id: str, device_id: str, token: str) -> bool:
        stored_token: str = self._auth_repository.get_token(account_id, device_id)
        
        if stored_token:
            return stored_token.decode("utf-8") == token
        
        raise TokenNotFoundError("Token not found")
