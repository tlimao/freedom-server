from redis import Redis
from aiohttp.web import RouteDef, get, post

from freedomlib.account.account_repository import AccountRepository
from freedomlib.account.account_repository_impl import AccountRepositoryImpl
from freedomlib.account.account_manager import AccountManager
from freedomlib.key.key_repository import KeyRepository
from freedomlib.key.key_repository_impl import KeyRepositoryImpl
from freedomlib.key.key_manager import KeyManager
from freedomserver.context.account.account_service import AccountService
from freedomserver.context.account.account_controller import AccountController

class AccountRoutes:
    
    @classmethod
    def create(cls, redis_connection: Redis) -> list[RouteDef]:
        account_repository: AccountRepository = AccountRepositoryImpl(redis_connection)
        account_manager: AccountManager = AccountManager(account_repository)
        
        key_repository: KeyRepository = KeyRepositoryImpl(redis_connection)
        key_manager: KeyManager = KeyManager(key_repository)
        
        account_service: AccountService = AccountService(account_manager, key_manager)
        
        account_controller: AccountController = AccountController(account_service)
        
        return [
            post('/account', account_controller.create_account),
            get('/account/{aci}', account_controller.get_account)
        ]