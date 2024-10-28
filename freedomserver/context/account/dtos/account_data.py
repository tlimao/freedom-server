from dataclasses import dataclass

from freedomlib.utils.serializable import Serializable

@dataclass(frozen=True)
class AccountData(Serializable):
    
    aci: str
    nick: str
    email: str
    phonenumber: str
    ed25519_public_key: str
    x25519_public_key: str
    discoverable: bool = True
    pin_hash: str = None
    
    @classmethod
    def from_dict(cls, data: dict) -> 'AccountData':
        return AccountData(**data)
    
    def to_dict(self) -> dict:
        return self.__dict__