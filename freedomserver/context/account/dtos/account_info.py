from dataclasses import dataclass


@dataclass(frozen=True)
class AccountInfo:
    
    nick: str
    email: str
    phonenumber: str
    ed25519_pub_key: str
    discoverable: bool = True
    pin_hash: str = None