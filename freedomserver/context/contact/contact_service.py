from typing import List

from freedomlib.contact.contact import Contact
from freedomlib.account.account import Account

from freedomserver.context.account.repository.account_repository import AccountRepository
from freedomserver.context.contact.errors.contact_error import ContactNotFoundError
from freedomserver.context.key.repository.key_repository import KeyRepository

class ContactService:
    
    def __init__(self, account_repository: AccountRepository, key_repository: KeyRepository) -> None:
        self._account_repository: AccountRepository = account_repository
        self._key_repository: KeyRepository = key_repository

    def get_contacts(self, phonenumbers: List[str], acis: List[str]) -> List[Contact]:
        contacts: List[Contact] = []
        
        for phonenumber in phonenumbers:
            try:
                contacts.append(self._get_contact_by_phonenumber(phonenumber))
                
            except Exception:
                pass
        
        for aci in acis:
            try:
                contacts.append(self._get_contact_by_aci(aci))
            except Exception:
                pass
            
        return contacts

    def _get_contact_by_phonenumber(self, phonenumber: str) -> Contact:
        try:
            account: Account = self._account_repository.get_by_phonenumber(phonenumber)
            
            if not account:
                raise ContactNotFoundError("Phonenumber not found")
        
            return Contact(
                aci=account.aci,
                nick=account.nick,
                email=account.email,
                phonenumber=account.phonenumber
            )
        
        except Exception as e:
            raise ContactNotFoundError(message=e)

    def _get_contact_by_aci(self, aci: str) -> Contact:
        try:
            account: Account = self._account_repository.get_by_aci(aci)
            
            if not account:
                raise ContactNotFoundError("ACI not found")
        
            return Contact(
                aci=account.aci,
                nick=account.nick,
                email=account.email,
                phonenumber=account.phonenumber
            )
            
        except Exception as e:
            raise ContactNotFoundError(message=e)