from dataclasses import dataclass


@dataclass(frozen=True)
class AccountInfo:
    
    nick: str
    email: str
    phonenumber: str
    pub_key: str
    discoverable: bool = True
    pin_hash: str = None