from freedomserver.configuration.server_keys import ServerKeys
from freedomserver.context.auth.auth_repository import AuthRepository
from freedomlib.key.key_repository import KeyRepository
from freedomlib.key.key import Key
from freedomserver.context.auth.dtos.auth_challenge import AuthChallenge
from freedomserver.context.auth.dtos.auth_verify import AuthVerify
from freedomserver.context.auth.error.challenge_signature_not_valid_error import ChallengeSignatureNotValidError
from freedomserver.context.auth.error.token_not_found_error import TokenNotFoundError
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
from cryptography.hazmat.primitives import serialization
import base64
import secrets

from freedomserver.context.utils.conversions import str_to_bytes
from freedomserver.context.utils.generate_ids import generate_number_id_str

class AuthService:
    
    CHALLENGE_SIZE: int  = 32
    
    def __init__(self, server_keys: ServerKeys, auth_repository: AuthRepository, key_repository: KeyRepository):
        self._server_keys: ServerKeys = server_keys
        self._auth_repository: AuthRepository = auth_repository
        self._key_repository: KeyRepository = key_repository

    def get_challenge(self, aci: str, device_id: str) -> AuthChallenge:
        request_id: str = generate_number_id_str(size=10)
        challenge: str = secrets.token_urlsafe(self.CHALLENGE_SIZE)
        signature: str = self._server_keys.sign_b64_str(f"{request_id}.{challenge}")
        
        self._auth_repository.store_challenge(aci, device_id, challenge)
        
        return AuthChallenge(request_id, challenge, signature)

    def verify_challenge(self, aci: str, device_id: str, challenge: str, signature: str) -> str:
        key: Key = self._key_repository.get_key_by_aci(aci)
        
        self._verify_challenge_signature(key, aci, device_id, challenge, signature)
        
        token: str = secrets.token_urlsafe(32)
        
        self._auth_repository.store_token(aci, device_id, token)
        
        return AuthVerify(token)
        
    def _verify_challenge_signature(self, key: Key, aci: str, device_id: str, challenge: str, signature: str) -> bool:
        try:
            # Obter o desafio original do repositório
            challenge_stored: str = self._auth_repository.get_challenge(aci, device_id)
            
            if challenge_stored != challenge:
                raise ChallengeSignatureNotValidError("Challenge expired!")
            
            # Carregar a chave pública do formato PEM
            public_key: Ed25519PublicKey = serialization.load_pem_public_key(key.ed25519_pub_key.encode())
            
            # Decodificar o desafio assinado de base64
            signature: bytes = base64.b64decode(signature)
            
            # Verificar a assinatura
            public_key.verify(signature, challenge.encode())

            return True
        except Exception as e:
            # Se a verificação falhar, lançar uma exceção personalizada
            raise ChallengeSignatureNotValidError("A assinatura do desafio não é válida") from e

    def verify_token(self, aci: str, device_id: str, token: str) -> bool:
        stored_token: bytes = self._auth_repository.get_token(aci, device_id)
        
        if stored_token:
            return stored_token.decode("utf-8") == token
        
        raise TokenNotFoundError("Token not found")
