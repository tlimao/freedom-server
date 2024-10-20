import json
import logging

from freedomlib.account.account import Account
from freedomlib.account.account_repository import AccountRepository
from freedomlib.key.key import Key
from freedomlib.key.key_repository import KeyRepository

from freedomserver.context.account.account_cache import AccountCache
from freedomserver.context.account.dtos.account_data import AccountData
from freedomserver.context.account.dtos.account_info import AccountInfo
from freedomserver.context.account.dtos.account_profile import AccountProfile
from freedomserver.context.account.dtos.account_registration import AccountRegistration
from freedomserver.context.account.dtos.account_verification import AccountVerification
from freedomserver.context.account.errors.account_error import AccountNotCreatedError, AccountRegistrationError, AccountUpdateError, AccountVerificationError, AccountNotFoundError
from freedomserver.context.utils.generate_ids import generate_number_id_str, generate_uuid7_str, generate_verification_code
from freedomserver.context.utils.mail_sender import MailSender

class AccountService:
    
    def __init__(self, account_repository: AccountRepository, account_cache: AccountCache, key_repository: KeyRepository, mail_sender: MailSender):
        self._account_repository: AccountRepository  = account_repository
        self._account_cache: AccountCache = account_cache
        self._key_repository: KeyRepository = key_repository
        self._mail_sender: MailSender = mail_sender
        
    def register_account(self, phonenumber: str, email: str) -> AccountRegistration:
        try:
            account_lock: bool = False

            account: Account = self._account_repository.get_by_phonenumber(phonenumber)
            
            if account:
                account_lock = account.pin_hash != None

            request_id: str = generate_number_id_str()
            verification_code: str = generate_verification_code()
            
            verification_code_send: bool = self._send_verification_code(email, verification_code)
            
            if not verification_code_send:
                raise AccountRegistrationError("Can't send email!")
            
            self._account_cache.set(
                f"account:registration:{phonenumber}",
                json.dumps({
                    "request_id": request_id,
                    "verification_code": verification_code,
                    "account_lock": account_lock
                }))
            
            return AccountRegistration(
                request_id=request_id,
                account_lock=account_lock)

        except Exception as e:
            raise AccountRegistrationError(message=e)

    def verify_account(self, request_id: str, verification_code: str, phonenumber: str) -> AccountVerification:
        try:
            registration_data: dict = self._account_cache.get(f"account:registration:{phonenumber}")
            
            if not registration_data:
                raise AccountVerificationError("Verification invalid!")
            
            if request_id != registration_data.get("request_id"):
                raise AccountVerificationError("Request id invalid!")

            if verification_code != registration_data.get("verification_code"):
                raise AccountVerificationError("Verification code invalid!")

            verification_id: str = generate_number_id_str()

            self._account_cache.set(
                f"account:verification:{phonenumber}",
                json.dumps({
                    "request_id": verification_id,
                    "account_lock": registration_data.get("account_lock")
                }))

            return AccountVerification(
                verification_id=verification_id,
                account_lock=registration_data.get("account_lock"))
            
        except Exception as e:
            raise AccountVerificationError(message=e)

    def create_account(self, request_id: str, account_info: AccountInfo) -> AccountData:
        try:
            old_key: Key = None
            
            verification_data: dict = self._account_cache.get(f"account:verification:{account_info.phonenumber}")
            
            if not verification_data:
                raise AccountNotCreatedError("Verification invalid!")
            
            if request_id != verification_data.get("request_id"):
                raise AccountNotCreatedError("Request id invalid!")

            if verification_data.get("account_lock"):
                account: Account = self._account_repository.get_by_phonenumber(account_info.phonenumber)
                
                if account_info.pin_hash != account.pin_hash:
                    raise AccountNotCreatedError("Incorrect PIN!")
                
                old_key: Key = self._key_repository.get_key_by_aci(account.aci)
            
            else:
                account: Account = Account(
                    aci=generate_uuid7_str(),
                    nick=account_info.nick,
                    email=account_info.email,
                    phonenumber=account_info.phonenumber,
                    discoverable=account_info.discoverable,
                    pin_hash=account_info.pin_hash,
                )
            
            self._account_repository.save(account)
            
            if old_key:
                self._key_repository.delete(old_key.id)

            key: Key = Key(
                id=generate_uuid7_str(),
                aci=account.aci,
                pub_key=account_info.pub_key
            )
            
            self._key_repository.save(key)
            
            
            self._account_cache.delete(f"account:verification:{account_info.phonenumber}")
            self._account_cache.delete(f"account:registration:{account_info.phonenumber}")
            
            return AccountData(
                aci=account.aci,
                nick=account.nick,
                email=account.email,
                phonenumber=account.phonenumber,
                pub_key=account_info.pub_key,
                discoverable=account.discoverable,
                pin_hash=account.pin_hash,
            )
            
        except Exception as e:
            raise AccountNotCreatedError(message=e)

    def get_profile(self, aci: str) -> AccountProfile:
        try:
            account: Account = self._account_repository.get_by_aci(aci)
            
            if not account:
                raise AccountNotFoundError("Account not exists!")
            
            return AccountProfile(
                aci=account.aci,
                nick=account.nick,
                discoverable=account.discoverable
            )
            
        except Exception as e:
            raise AccountNotFoundError(message=e)

    def update_profile(self, account_profile: AccountProfile) -> AccountProfile:
        try:
            account: Account = self._account_repository.get_by_aci(account_profile.aci)
            
            if not account:
                raise AccountNotFoundError("Account not exists!")
            
            updated_account: Account = Account(
                aci=account.aci,
                nick=account_profile.nick,
                email=account.email,
                phonenumber=account.phonenumber,
                discoverable=account_profile.discoverable,
                pin_hash=account.pin_hash,
            )
            
            self._account_repository.update(updated_account)
            
            return AccountProfile(
                aci=updated_account.aci,
                nick=updated_account.nick,
                discoverable=updated_account.discoverable
            )
            
        except AccountUpdateError as e:
            raise AccountUpdateError(message=e)
        
    def _send_verification_code(self, email: str, verification_code: str) -> bool:
        try:
            self._mail_sender.send_email(
                message=f"Verification Code\n\n{verification_code}",
                to=email,
                sender="noreplay@freedom.com",
                sender_name="Freedom Messaging",
                subject="Verification Code"
            )
            
            return True
        except Exception as e:
            logging.error(e)
            
            return False
