from dataclasses import dataclass


@dataclass
class RegistrationRequest:
    
    phonenumber: str
    email: str

    @classmethod
    def from_dict(cls, data: dict) -> 'RegistrationRequest':
        return RegistrationRequest(
            phonenumber=data.get('phonenumber'),
            email=data.get('email')
        )
        