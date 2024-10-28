from typing import List

from freedomlib.contact.contact import Contact
from freedomlib.account.account import Account
from freedomlib.key.key_box import KeyBox

from freedomserver.context.account.repository.account_repository import AccountRepository
from freedomserver.context.contact.errors.contact_error import ContactNotFoundError
from freedomserver.context.key.repository.key_repository import KeyRepository

class ContactService:
    
    def __init__(self, account_repository: AccountRepository, key_repository: KeyRepository) -> None:
        self._account_repository: AccountRepository = account_repository
        self._key_repository: KeyRepository = key_repository

    def get_contacts(self, phonenumbers: List[str]) -> List[Contact]:
        contacts: List[Contact] = []
        
        for phonenumber in phonenumbers:
            try:
                contacts.append(self._get_contact(phonenumber))
                
            except Exception:
                pass
            
        return contacts

    def _get_contact(self, phonenumber: str) -> Contact:
        try:
            account: Account = self._account_repository.get_by_phonenumber(phonenumber)
            
            if not account:
                raise ContactNotFoundError("Phonenumber not found")
            
            key_box: KeyBox = self._key_repository.get_key_by_aci(account.aci)
            
            if not key_box:
                raise ContactNotFoundError("Pub Key not found")
        
            return Contact(
                aci=account.aci,
                nick=account.nick,
                email=account.email,
                phonenumber=account.phonenumber
            )
        
        except Exception as e:
            raise ContactNotFoundError(message=e)