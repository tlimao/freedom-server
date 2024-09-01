from dataclasses import dataclass

from freedomlib.account.account import Account

@dataclass
class CreateAccountResponse:
    
    account: Account
    pub_key: str
    
    def to_dict(self) -> dict:
        return {
            'account': self.account.to_dict(),
            'pub_key': self.pub_key
        }