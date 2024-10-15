import base64
import uuid6

from freedomlib.account.account import Account
from freedomlib.account.account_repository import AccountRepository
from freedomlib.key.key import Key
from freedomlib.key.key_repository import KeyRepository

from freedomserver.context.account.dtos.account_info import AccountInfo
from freedomserver.context.account.dtos.account_profile_info import AccountProfileInfo
from freedomserver.context.account.dtos.account_security_info import AccountSecurityInfo

class AccountService:
    
    def __init__(self, account_repository: AccountRepository, key_repository: KeyRepository):
        self._account_repository: AccountRepository  = account_repository
        self._key_repository: KeyRepository = key_repository

    def get_account(self, aci: str) -> Account:
        return self._account_repository.get_by_aci(aci)

    def create_account(self, account_info: AccountInfo) -> Account:
        account: Account = Account(
            aci=self._generate_id(),
            nick=account_info.nick,
            email=account_info.email,
            phonenumber=account_info.phonenumber,
            discoverable=account_info.discoverable or True,
            pin_hash=account_info.pin_hash
        )
        
        key: Key = Key(
            id=self._generate_id(),
            aci=account.aci,
            pub_key=account_info.pub_key
        )
        
        self._key_repository.save(key)
        
        return self._account_repository.save(account)

    def update_profile(self, account_profile_info: AccountProfileInfo) -> Account:
        account: Account = self._account_repository.get_by_aci(account_profile_info.aci)
       
        account.nick = account_profile_info.nick
        
        return self._account_repository.update(account)
    
    def update_security(self, account_security_info: AccountSecurityInfo) -> None:
        account: Account = self._account_repository.get_by_aci(account_security_info.aci)
        
        account.pin_hash = account_security_info.pin_hash
        account.email = account_security_info.email
        account.phonenumber = account_security_info.phonenumber
        
        return self._account_repository.update(account)

    def _generate_id(self) -> str:
        return base64.b64encode(uuid6.uuid7().bytes).decode('utf-8')
