from dataclasses import dataclass

from freedomlib.utils.serializable import Serializable

@dataclass
class AuthVerifyResponse(Serializable):
    
    token: str
    
    @classmethod
    def from_dict(cls, data: dict) -> 'AuthVerifyResponse':
        return AuthVerifyResponse(**data)
    
    def to_dict(self) -> dict:
        return self.__dict__