from aiohttp.web import RouteDef, post

from freedomserver.configuration.server_keys import ServerKeys
from freedomserver.context.auth.auth_controller import AuthController
from freedomserver.context.auth.auth_service import AuthService
from freedomserver.context.auth.repository.auth_repository import AuthRepository
from freedomserver.context.key.repository.key_repository import KeyRepository

class AuthRoutes:
    
    @classmethod
    def create(cls,
               server_keys: ServerKeys,
               auth_repository: AuthRepository,
               key_repository: KeyRepository) -> list[RouteDef]:

        auth_service: AuthService = AuthService(server_keys, auth_repository, key_repository)
        auth_controller: AuthController = AuthController(auth_service)
        
        return [
            post('/auth/challenge', auth_controller.challenge),
            post('/auth/verify', auth_controller.verify)
        ]