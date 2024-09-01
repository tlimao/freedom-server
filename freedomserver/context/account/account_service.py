from freedomlib.account.account_info import AccountInfo
from freedomlib.account.account_manager import AccountManager
from freedomlib.account.account import Account
from freedomlib.key.key_info import KeyInfo
from freedomlib.key.key import Key
from freedomlib.key.key_manager import KeyManager
from freedomlib.account.error.account_not_found_error import AccountNotFoundError

class AccountService:
    
    def __init__(self, account_manager: AccountManager, key_manager: KeyManager):
        self._account_manager: AccountManager = account_manager
        self._key_manager: KeyManager = key_manager

    def get_account(self, account_id: str) -> Account:
        return self._account_manager.get_account_by_id(account_id)

    def create_account(self, account_info: AccountInfo, pub_key: str) -> tuple[Account, Key]:
        # Verifica se a conta já existe
        try:
            existing_account: Account = self._account_manager.get_account_by_phonenumber(account_info.phonenumber)
            # Se a conta existir, retorna a conta existente
            existing_key: Key = self._key_manager.get_account_key(existing_account.id)
            
            return existing_account, existing_key
        except AccountNotFoundError:
            # Se a conta não existir, cria uma nova
            account: Account = self._account_manager.create_account(account_info)
        
            key_info: KeyInfo = KeyInfo(
                account_id=account.id,
                pub_key=pub_key
            )
            
            key: Key = self._key_manager.put_key(key_info)
            
            return account, key