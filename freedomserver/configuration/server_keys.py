import base64
from dataclasses import dataclass, field

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey, Ed25519PrivateKey
from cryptography.hazmat.primitives import serialization

@dataclass
class ServerKeys:
    
    public_key: str
    private_key: str
    
    _public_key: Ed25519PublicKey = field(init=False, repr=False)
    _private_key: Ed25519PrivateKey = field(init=False, repr=False)
    
    def __post_init__(self):
        # Converte a string PEM da chave pública para o objeto Ed25519PublicKey
        self._public_key = serialization.load_pem_public_key(
            self.public_key.encode("utf-8")
        )
        
        # Converte a string PEM da chave privada para o objeto Ed25519PrivateKey
        self._private_key = serialization.load_pem_private_key(
            self.private_key.encode("utf-8"), 
            password=None
        )

    def get_public_key(self) -> Ed25519PublicKey:
        """Retorna a chave pública como um objeto Ed25519PublicKey."""
        return self._public_key
    
    def get_private_key(self) -> Ed25519PrivateKey:
        """Retorna a chave privada como um objeto Ed25519PrivateKey."""
        return self._private_key
    
    def get_public_key_pem(self) -> str:
        """Retorna a chave pública em formato PEM."""
        return self.public_key
    
    def get_private_key_pem(self) -> str:
        """Retorna a chave privada em formato PEM."""
        return self.private_key
    
    def sign(self, string: str) -> bytes:
        return self._private_key.sign(string.encode('utf-8'))

    def sign_b64_str(self, string: str) -> str:
        return base64.b64encode(self.sign(string)).decode("utf-8")