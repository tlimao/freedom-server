from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey
from cryptography.hazmat.primitives import serialization

def generate_server_keys() -> None:
    private_key: Ed25519PrivateKey = Ed25519PrivateKey.generate()
    public_key: Ed25519PublicKey = private_key.public_key()

    private_key_pem: str = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    ).decode('utf-8')

    public_key_pem: str = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ).decode('utf-8')

    print("="*93)
    print("="*40 + " SERVER KEYS " + "="*40)
    print("="*93 + "\n")
    print("Private Key:\n%s" % private_key_pem)
    print("Public Key:\n%s" % public_key_pem)
    print("="*93)
    print("="*30 + " !!! DON'T SHARE PRIVATE KEY !!! " + "="*30)
    print("="*93)