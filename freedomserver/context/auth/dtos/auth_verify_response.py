from dataclasses import dataclass

from freedomlib.utils.serializable import Serializable

@dataclass
class AuthVerifyResponse(Serializable):
    
    token: str
    
    def to_dict(self) -> dict:
        return self.__dict__