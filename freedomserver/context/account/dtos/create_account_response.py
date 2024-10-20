from dataclasses import dataclass

from freedomlib.utils.serializable import Serializable

from freedomserver.context.account.dtos.account_data import AccountData

@dataclass
class CreateAccountResponse(Serializable):
    
    account_data: AccountData 
    
    def to_dict(self) -> dict:
        return {
            "account_data": self.account_data.to_dict()
        }