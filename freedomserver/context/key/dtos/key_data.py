from dataclasses import dataclass


@dataclass
class KeyData:
    
    aci: str
    ed25519_public_key: str
    x25519_public_key: str