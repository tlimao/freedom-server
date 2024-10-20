from redis import Redis
from aiohttp.web import RouteDef, post

from freedomlib.key.key_repository import KeyRepository
from freedomserver.context.auth.auth_controller import AuthController
from freedomserver.context.auth.auth_service import AuthService
from freedomserver.context.auth.auth_repository import AuthRepository

class AuthRoutes:
    
    @classmethod
    def create(cls, auth_repository: AuthRepository, key_repository: KeyRepository) -> list[RouteDef]:
        auth_service: AuthService = AuthService(auth_repository, key_repository)
        auth_controller: AuthController = AuthController(auth_service)
        
        return [
            post('/auth/challenge', auth_controller.challenge),
            post('/auth/verify', auth_controller.verify)
        ]