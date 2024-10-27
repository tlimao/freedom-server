from dataclasses import dataclass

from freedomlib.utils.serializable import Serializable

@dataclass(frozen=True)
class AccountData(Serializable):
    
    aci: str
    nick: str
    email: str
    phonenumber: str
    ed25519_pub_key: str
    discoverable: bool = True
    pin_hash: str = None
    
    def to_dict(self) -> dict:
        return self.__dict__