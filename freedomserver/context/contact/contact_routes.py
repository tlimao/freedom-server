from redis import Redis
from aiohttp.web import RouteDef, get, post

from freedomlib.account.account_repository import AccountRepository
from freedomlib.account.account_repository_impl import AccountRepositoryImpl
from freedomlib.account.account_manager import AccountManager
from freedomlib.key.key_repository import KeyRepository
from freedomlib.key.key_repository_impl import KeyRepositoryImpl
from freedomlib.key.key_manager import KeyManager
from freedomserver.context.contact.contact_service import ContactService
from freedomserver.context.contact.contact_controller import ContactController
class ContactRoutes:

    @classmethod
    def create(cls, redis_connection: Redis) -> list[RouteDef]:
        account_repository: AccountRepository = AccountRepositoryImpl(redis_connection)
        account_manager: AccountManager = AccountManager(account_repository)
        
        key_repository: KeyRepository = KeyRepositoryImpl(redis_connection)
        key_manager: KeyManager = KeyManager(key_repository)
        
        contact_service: ContactService = ContactService(account_manager, key_manager)
        
        contact_controller: ContactController = ContactController(contact_service)
        
        return [
            post('/api/v1/contacts', contact_controller.contacts_info),
            get('/api/v1/contacts/{contact_id}', contact_controller.contact_info_by_id)
        ]