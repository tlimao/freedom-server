from dataclasses import dataclass


@dataclass
class AccountRegistration:
    
    registration_id: str
    account_lock: bool