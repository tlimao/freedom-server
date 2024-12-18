from aiohttp.web import RouteDef, get, post

from freedomserver.context.account.repository.account_repository import AccountRepository
from freedomserver.context.contact.contact_controller import ContactController
from freedomserver.context.contact.contact_service import ContactService
from freedomserver.context.key.repository.key_repository import KeyRepository

class ContactRoutes:
    
    @classmethod
    def create(cls,
               account_repository: AccountRepository,
               key_repository: KeyRepository) -> list[RouteDef]:
        
        contact_service: ContactService = ContactService(account_repository, key_repository)
        
        contact_controller: ContactController = ContactController(contact_service)
        
        return [
            post('/contact', contact_controller.fetch_contacts)
        ]