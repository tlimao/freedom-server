from dataclasses import dataclass

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey, Ed25519PrivateKey
from cryptography.hazmat.primitives import serialization

@dataclass
class ServerKeys:
    
    public_key: str
    private_key: str

    def get_public_key(self) -> Ed25519PublicKey:
        """Retorna a chave pública como um objeto Ed25519PublicKey."""
        return serialization.load_pem_public_key(
            self.public_key.encode("utf-8")
        )
    
    def get_private_key(self) -> Ed25519PrivateKey:
        """Retorna a chave privada como um objeto Ed25519PrivateKey."""
        return serialization.load_pem_private_key(
            self.private_key.encode("utf-8"), 
            password=None
        )
    
    def get_public_key_pem(self) -> str:
        """Retorna a chave pública em formato PEM."""
        return self.public_key
    
    def get_private_key_pem(self) -> str:
        """Retorna a chave privada em formato PEM."""
        return self.private_key