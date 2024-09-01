import json
from dataclasses import dataclass

from freedomlib.account.account_info import AccountInfo
from freedomlib.account.account import Account

@dataclass
class CreateAccountRequest:
    account_info: AccountInfo
    pub_key: str

    @classmethod
    def from_dict(cls, data: dict) -> 'CreateAccountRequest':
        return cls(
            account_info=AccountInfo(**data['account_info']),
            pub_key=data['pub_key']
        )

    def to_dict(self) -> dict:
        return {
            'account_info': self.account_info.to_dict(),
            'pub_key': self.pub_key
        }

@dataclass
class CreateAccountResponse:
    
    account: Account
    pub_key: str
    
    def to_dict(self) -> dict:
        return {
            'account': self.account.to_dict(),
            'pub_key': self.pub_key
        }