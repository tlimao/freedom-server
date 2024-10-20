from aiohttp.web import RouteDef, get, post, put

from freedomlib.account.account_repository import AccountRepository
from freedomlib.key.key_repository import KeyRepository
from freedomserver.context.account.account_cache import AccountCache
from freedomserver.context.account.account_service import AccountService
from freedomserver.context.account.account_controller import AccountController
from freedomserver.context.utils.mail_sender import MailSender

class AccountRoutes:
    
    @classmethod
    def create(cls, 
               mail_sender: MailSender, 
               account_repository: AccountRepository, 
               account_cache: AccountCache, 
               key_repository: KeyRepository) -> list[RouteDef]:

        account_service: AccountService = AccountService(
            account_repository=account_repository,
            account_cache=account_cache,
            key_repository=key_repository,
            mail_sender=mail_sender,
        )
        
        account_controller: AccountController = AccountController(account_service)
        
        return [
            post('/account/register', account_controller.register),
            post('/account/verify', account_controller.verify),
            post('/account/create', account_controller.create),
            get('/account/profile/{aci}', account_controller.get_profile),
            put('/account/profile', account_controller.update_profile)
        ]