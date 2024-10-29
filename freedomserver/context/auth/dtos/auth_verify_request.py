from dataclasses import dataclass

from freedomlib.utils.serializable import Serializable

@dataclass
class AuthVerifyRequest(Serializable):
    
    request_id: str
    aci: str
    device_id: str
    challenge: str
    signature: str
    
    @classmethod
    def from_dict(cls, data: dict) -> 'AuthVerifyRequest':
        return AuthVerifyRequest(
            request_id=data.get("request_id"),
            aci=data.get("aci"),
            device_id=data.get("device_id"),
            challenge=data.get("challenge"),
            signature=data.get("signature")
        )

    def to_dict(self) -> dict:
        return self.__dict__