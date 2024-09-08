from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization

class ServerKeys:
    
    def __init__(self) -> None:
        self._server_private_key: ed25519.Ed25519PrivateKey = ed25519.Ed25519PrivateKey.generate()
        self._server_public_key: ed25519.Ed25519PublicKey = self._server_private_key.public_key()

    def get_server_private_key(self) -> ed25519.Ed25519PrivateKey:
        return self._server_private_key

    def get_server_public_key(self) -> ed25519.Ed25519PublicKey:
        return self._server_public_key

    def get_server_public_key_pem(self) -> str:
        return self._server_public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode('utf-8')
