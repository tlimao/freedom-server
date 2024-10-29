from dataclasses import dataclass

from freedomlib.utils.serializable import Serializable

@dataclass
class AuthChallenge(Serializable):
    
    request_id: str
    challenge: str
    signature: str

    def to_dict(self) -> dict:
        return self.__dict__