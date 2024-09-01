import json
from dataclasses import dataclass

from freedomlib.account.account_info import AccountInfo

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

    def to_dict(self) -> str:
        return {
            'account_info': self.account_info.to_dict(),
            'pub_key': self.pub_key
        }