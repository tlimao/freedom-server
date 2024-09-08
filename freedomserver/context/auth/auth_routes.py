from redis import Redis
from aiohttp.web import RouteDef, post

from freedomserver.context.auth.auth_controller import AuthController
from freedomserver.context.auth.auth_service import AuthService
from freedomserver.context.auth.auth_repository import AuthRepository
from freedomserver.context.auth.auth_repository_impl import AuthRepositoryImpl
from freedomserver.context.server.server_keys import ServerKeys

from freedomlib.key.key_manager import KeyManager
from freedomlib.key.key_repository import KeyRepository
from freedomlib.key.key_repository_impl import KeyRepositoryImpl

class AuthRoutes:
    
    @classmethod
    def create(cls, redis_connection: Redis, server_keys: ServerKeys) -> list[RouteDef]:
        auth_repository: AuthRepository = AuthRepositoryImpl(redis_connection)
        key_repository: KeyRepository = KeyRepositoryImpl(redis_connection)
        key_manager: KeyManager = KeyManager(key_repository)
        auth_service: AuthService = AuthService(auth_repository, key_manager)
        auth_controller: AuthController = AuthController(auth_service, server_keys)
        
        return [
            post('/auth/challenge', auth_controller.get_challenge),
            post('/auth/verify', auth_controller.verify_challenge)
        ]