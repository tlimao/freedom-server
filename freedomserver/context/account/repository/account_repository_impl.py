import json
from freedomlib.account.account import Account
from redis import Redis

from freedomserver.context.account.repository.account_repository import AccountRepository
from freedomserver.context.account.errors.account_error import AccountNotFoundError


class AccountRepositoryImpl(AccountRepository):
    
    ACCOUNT_DIRECTORY: str = "account:aci"
    ACCOUNT_EMAIL_DIRECOTRY: str = "account:email"
    ACCOUNT_E164_DIRECOTRY: str = "account:e164"
    
    
    def __init__(self, redis_connection: Redis) -> None:
        self._redis_connection: Redis = redis_connection

    def save(self, account: Account) -> Account:        
        key: str = f"{self.ACCOUNT_DIRECTORY}:{account.aci}"
        
        self._redis_connection.set(key, json.dumps(account.to_dict()))
        
        key_e164: str = f"{self.ACCOUNT_E164_DIRECOTRY}:{account.phonenumber}"
        
        self._redis_connection.set(key_e164, account.aci)
        
        return account
    
    def get_by_aci(self, aci: str) -> Account | None:
        key: str = f"{self.ACCOUNT_DIRECTORY}:{aci}"
        account_data: str = self._redis_connection.get(key)
        
        if account_data:
            account: Account = Account.from_dict(json.loads(account_data))
            
            return account
        
        else:
            return None

    def get_by_email(self, email: str) -> Account | None:
        raise NotImplementedError()

    def get_by_phonenumber(self, phonenumber: str) -> Account | None:
        key: str = f"{self.ACCOUNT_E164_DIRECOTRY}:{phonenumber}"
        
        aci: bytes = self._redis_connection.get(key)
        
        if aci:
            return self.get_by_aci(aci.decode())
        else:
            return None

    def update(self, account: Account) -> Account:
        key: str = f"{self.ACCOUNT_DIRECTORY}:{account.aci}"
        
        self._redis_connection.set(key, json.dumps(account.to_dict()))
        
        return account

    def delete(self, aci: str) -> None:
        account: Account = self.get_by_aci(aci)
        
        key: str = f"{self.ACCOUNT_DIRECTORY}:{account.aci}"
        
        self._redis_connection.delete(key)
               
        key_e164: str = f"{self.ACCOUNT_E164_DIRECOTRY}:{account.phonenumber}"
        
        self._redis_connection.delete(key_e164)

    