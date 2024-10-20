from dataclasses import dataclass

from freedomserver.context.account.dtos.account_info import AccountInfo


@dataclass
class CreateAccountRequest:
    
    account_info: AccountInfo
    request_id: str
    
    @classmethod
    def from_dict(cls, data: dict) -> 'CreateAccountRequest':
        return CreateAccountRequest(
            account_info=AccountInfo(**data.get("account_info")),
            request_id=data.get("request_id")
        )