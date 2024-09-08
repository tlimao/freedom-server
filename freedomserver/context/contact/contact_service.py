from aiohttp.web import Request

from freedomlib.contact.contact import Contact
from freedomlib.account.account_manager import AccountManager
from freedomlib.key.key_manager import KeyManager
from freedomlib.account.account import Account
from freedomlib.key.key import Key
from freedomlib.account.error.account_not_found_error import AccountNotFoundError

class ContactService:

    def __init__(self, account_manager: AccountManager, key_manager: KeyManager) -> None:
        self._account_manager: AccountManager = account_manager
        self._key_manager: KeyManager = key_manager

    def get_contacts(self, account_phonenumbers: list[str]) -> list[Contact]:
        contacts: list[Contact] = []
        
        for phonenumber in account_phonenumbers:
            try:
                account: Account = self._account_manager.get_account_by_phonenumber(phonenumber)
                key: Key = self._key_manager.get_account_key(account.id)
                
                contacts.append(Contact(
                    id=account.id,
                    nick=account.nick,
                    email=account.email,
                    phonenumber=account.phonenumber,
                    pub_key=key.pub_key
                ))
            except AccountNotFoundError:
                pass
        
        return contacts

    def get_contact_by_id(self, contact_id: str) -> Contact:
        try:
            account: Account = self._account_manager.get_account_by_id(contact_id)
            key: Key = self._key_manager.get_account_key(account.id)
            
            return Contact(
                id=account.id,
                nick=account.nick,
                email=account.email,
                phonenumber=account.phonenumber,
                pub_key=key.pub_key
            )
        except AccountNotFoundError:
            raise ValueError(f"Contact with id {contact_id} not found")