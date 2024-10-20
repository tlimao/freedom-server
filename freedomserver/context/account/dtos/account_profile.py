from dataclasses import dataclass

from freedomlib.utils.serializable import Serializable

@dataclass
class AccountProfile(Serializable):
    
    aci: str
    nick: str
    discoverable: bool

    def to_dict(self) -> dict:
        return self.__dict__

    @classmethod
    def from_dict(cls, data: dict) -> 'AccountProfile':
        return AccountProfile(
            aci=data.get('aci'),
            nick=data.get('nick'),
            discoverable=data.get('discoverable')
        )