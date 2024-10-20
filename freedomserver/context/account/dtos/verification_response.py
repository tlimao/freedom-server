from dataclasses import dataclass

from freedomlib.utils.serializable import Serializable

@dataclass
class VerificationResponse(Serializable):
    
    verification_id: str
    account_lock: bool
    
    def to_dict(self) -> dict:
        return self.__dict__