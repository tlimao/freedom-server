from dataclasses import dataclass

from freedomlib.utils.serializable import Serializable


@dataclass
class AuthChallengeResponse(Serializable):
    
    request_id: str
    challenge: str
    signature: str
    
    @classmethod
    def from_dict(cls, data: dict) -> 'AuthChallengeResponse':
        return AuthChallengeResponse(**data)

    def to_dict(self) -> dict:
        return self.__dict__