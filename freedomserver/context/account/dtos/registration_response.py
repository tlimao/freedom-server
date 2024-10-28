from dataclasses import dataclass

from freedomlib.utils.serializable import Serializable

@dataclass
class RegistrationResponse(Serializable):

    request_id: str
    account_lock: bool

    @classmethod
    def from_dict(cls, data:dict) -> 'RegistrationResponse':
        return RegistrationResponse(**data)

    def to_dict(self) -> dict:
        return self.__dict__