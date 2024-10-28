from dataclasses import dataclass

from freedomlib.utils.serializable import Serializable

from freedomserver.context.account.dtos.account_data import AccountData

@dataclass
class CreateAccountResponse(Serializable):
    
    account_data: AccountData 
    
    @classmethod
    def from_dict(cls, data: dict) -> 'CreateAccountResponse':
        return CreateAccountResponse(
            account_data=AccountData.from_dict(data.get("account_data"))
        )
    
    def to_dict(self) -> dict:
        return {
            "account_data": self.account_data.to_dict()
        }