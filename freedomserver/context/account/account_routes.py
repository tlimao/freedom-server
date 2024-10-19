from redis import Redis
from aiohttp.web import RouteDef, get, post, put

from freedomlib.account.account_repository import AccountRepository
from freedomserver.context.account.account_repository_impl import AccountRepositoryImpl
from freedomserver.context.account.account_service import AccountService
from freedomserver.context.account.account_controller import AccountController
from freedomserver.context.utils.mail_sender import MailSender

class AccountRoutes:
    
    @classmethod
    def create(cls, mail_sender: MailSender, redis_connection: Redis) -> list[RouteDef]:
        account_repository: AccountRepository = AccountRepositoryImpl(redis_connection)

        account_service: AccountService = AccountService(
            account_repository=account_repository,
            mail_sender=mail_sender,
        )
        
        account_controller: AccountController = AccountController(account_service)
        
        return [
            post('/account/register', account_controller.register),
            post('/account/verify', account_controller.verify),
            post('/account', account_controller.create),
            get('/account/{aci}', account_controller.get_account),
            get('/account/profile', account_controller.profile),
            put('/account/profile', account_controller.update_profile),
            put('/account/privacy', account_controller.update_privacy)
        ]