from dataclasses import dataclass


@dataclass
class KeyData:
    
    aci: str
    ed25519_pub_key: str
    x25519_pub_key: str