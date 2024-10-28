from freedomlib.crypto.functions import ED25519

def generate_server_keys() -> None:
    private_key, public_key = ED25519.create_key_pair()
    private_key_pem: str = ED25519.private_key_to_pem(private_key)
    public_key_pem: str = ED25519.public_key_to_pem(public_key)

    print("="*93)
    print("="*40 + " SERVER KEYS " + "="*40)
    print("="*93 + "\n")
    print("Private Key:\n%s" % private_key_pem)
    print("Public Key:\n%s" % public_key_pem)
    print("="*93)
    print("="*30 + " !!! DON'T SHARE PRIVATE KEY !!! " + "="*30)
    print("="*93)