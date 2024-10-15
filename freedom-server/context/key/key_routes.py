from redis import Redis
from aiohttp.web import RouteDef, get, put

from freedomlib.key.key_repository import KeyRepository
from freedomlib.key.key_repository_impl import KeyRepositoryImpl
from freedomlib.key.key_manager import KeyManager

from freedomserver.context.key.key_controller import KeyController

class KeyRoutes:
    
    @classmethod
    def create(cls, redis_connection: Redis) -> list[RouteDef]:
        key_repository: KeyRepository = KeyRepositoryImpl(redis_connection)
        key_manager: KeyManager = KeyManager(key_repository)
        
        key_controller: KeyController = KeyController(key_manager)
        
        return [
            get('/key/{account_id}', key_controller.get_account_key)
        ]