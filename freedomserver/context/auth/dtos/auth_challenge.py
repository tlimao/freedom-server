from dataclasses import dataclass


@dataclass
class AuthChallenge:
    
    request_id: str
    challenge: str
    signature: str