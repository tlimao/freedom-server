import json
from freedomlib.account.account import Account
from freedomlib.account.account_repository import AccountRepository
from redis import Redis

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
        
        key_email: str = f"{self.ACCOUNT_EMAIL_DIRECOTRY}:{account.email}"
        
        self._redis_connection.set(key_email, account.aci)
        
        key_e164: str = f"{self.ACCOUNT_E164_DIRECOTRY}:{account.phonenumber}"
        
        self._redis_connection.set(key_e164, account.aci)
        
        return account
    
    def get_by_aci(self, aci: str) -> Account:
        key: str = f"{self.ACCOUNT_DIRECTORY}:{aci}"
        account_data: str = self._redis_connection.get(key)
        
        if account_data:
            account: Account = Account.from_dict(json.loads(account_data))
            
            return account
        
        else:
            raise AccountNotFoundError()

    def get_by_email(self, email: str) -> Account:
        key: str = f"{self.ACCOUNT_EMAIL_DIRECOTRY}:{email}"
        
        aci: str = json.loads(self._redis_connection.get(key))
        
        return self.get_by_aci(aci)

    def get_by_phonenumber(self, phonenumber: str) -> Account:
        key: str = f"{self.ACCOUNT_EMAIL_DIRECOTRY}:{phonenumber}"
        
        aci: str = json.loads(self._redis_connection.get(key))
        
        return self.get_by_aci(aci)

    def update(self, account: Account) -> Account:
        key: str = f"{self.ACCOUNT_DIRECTORY}:{account.aci}"
        
        self._redis_connection.set(key, json.dumps(account.to_dict()))
        
        return account

    def delete(self, aci: str) -> None:
        account: Account = self.get_by_aci(aci)
        
        key: str = f"{self.ACCOUNT_DIRECTORY}:{account.aci}"
        
        self._redis_connection.delete(key)
        
        key_email: str = f"{self.ACCOUNT_EMAIL_DIRECOTRY}:{account.email}"
        
        self._redis_connection.delete(key_email)
        
        key_e164: str = f"{self.ACCOUNT_E164_DIRECOTRY}:{account.phonenumber}"
        
        self._redis_connection.delete(key_e164)

    