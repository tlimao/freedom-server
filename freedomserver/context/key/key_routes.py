from aiohttp.web import RouteDef, get

from freedomserver.context.key.repository.key_repository import KeyRepository
from freedomserver.context.key.key_service import KeyService
from freedomserver.context.key.key_controller import KeyController

class KeyRoutes:
    
    @classmethod
    def create(cls, key_repository: KeyRepository) -> list[RouteDef]:
        key_service: KeyService = KeyService(key_repository)
        
        key_controller: KeyController = KeyController(key_service)
        
        return [
            get('/key/{aci}', key_controller.get_key)
        ]