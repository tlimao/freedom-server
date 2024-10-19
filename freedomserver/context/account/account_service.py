import base64
import uuid6

from freedomlib.account.account import Account
from freedomlib.account.account_repository import AccountRepository
from freedomlib.key.key import Key
from freedomlib.key.key_repository import KeyRepository

from freedomserver.context.account.dtos.account_info import AccountInfo
from freedomserver.context.account.dtos.account_profile_info import AccountProfileInfo
from freedomserver.context.account.dtos.account_registration import AccountRegistration
from freedomserver.context.account.dtos.account_security_info import AccountSecurityInfo
from freedomserver.context.account.errors.account_error import AccountNotFoundError, AccountRegistrationError
from freedomserver.context.utils.generate_ids import generate_number_id_str, generate_uuid7_str, generate_verification_code
from freedomserver.context.utils.mail_sender import MailSender

class AccountService:
    
    def __init__(self, account_repository: AccountRepository, mail_sender: MailSender):
        self._account_repository: AccountRepository  = account_repository
        self._mail_sender: MailSender = mail_sender
        
    def register_account(self, phonenumber: str, email: str) -> AccountRegistration:
        try:
            account_lock: bool = False

            account: Account = self._account_repository.get_by_phonenumber(phonenumber)
            
            if account:
                account_lock = account.pin_hash != None

            registration_id: str = generate_number_id_str()
            verification_token: str = generate_verification_code()
            
            self._mail_sender.send_email(
                message=f"Verification Code\n\n{verification_token}",
                to=email,
                sender="noreplay@freedom.com",
                sender_name="Freedom Messaging",
                subject="Verification Code"
            )
            
            return AccountRegistration(
                registration_id=registration_id,
                account_lock=account_lock
            )

        except Exception as e:
            raise AccountRegistrationError(message=e)

    def get_account(self, aci: str) -> Account:
        ...

    def create_account(self, account_info: AccountInfo) -> Account:
        ...

    def update_profile(self, account_profile_info: AccountProfileInfo) -> Account:
        ...
    
    def update_security(self, account_security_info: AccountSecurityInfo) -> None:
        ...
