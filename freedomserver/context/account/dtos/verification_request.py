from dataclasses import dataclass


@dataclass
class VerificationRequest:
    
    request_id: str
    verification_code: str
    phonenumber: str

    @classmethod
    def from_dict(cls, data: dict) -> 'VerificationRequest':
        return VerificationRequest(
            request_id=data.get("request_id"),
            verification_code=data.get("verification_code"),
            phonenumber=data.get("phonenumber")
        )