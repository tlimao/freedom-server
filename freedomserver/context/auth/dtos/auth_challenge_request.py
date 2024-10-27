from dataclasses import dataclass


@dataclass
class AuthChallengeRequest:
    
    aci: str
    device_id: str
    
    @classmethod
    def from_dict(cls, data: dict) -> 'AuthChallengeRequest':
        return AuthChallengeRequest(
            aci=data.get('aci'),
            device_id=data.get('device_id')
        )
        