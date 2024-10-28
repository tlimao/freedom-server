from dataclasses import dataclass

from freedomlib.utils.serializable import Serializable
from freedomserver.context.account.dtos.account_info import AccountInfo


@dataclass
class CreateAccountRequest(Serializable):
    
    request_id: str
    account_info: AccountInfo
    
    @classmethod
    def from_dict(cls, data: dict) -> 'CreateAccountRequest':
        return CreateAccountRequest(
            request_id=data.get("request_id"),
            account_info=AccountInfo.from_dict(data.get("account_info"))
        )

    def to_dict(self) -> dict:
        return {
            "request_id": self.request_id,
            "account_info": self.account_info.to_dict(),
        }