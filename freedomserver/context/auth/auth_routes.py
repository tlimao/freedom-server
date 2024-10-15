from redis import Redis
from aiohttp.web import RouteDef, post

from freedomserver.context.auth.auth_controller import AuthController
from freedomserver.context.auth.auth_service import AuthService
from freedomserver.context.auth.auth_repository import AuthRepository
from freedomserver.context.auth.auth_repository_impl import AuthRepositoryImpl

class AuthRoutes:
    
    @classmethod
    def create(cls, redis_connection: Redis) -> list[RouteDef]:
        auth_repository: AuthRepository = AuthRepositoryImpl(redis_connection)
        auth_service: AuthService = AuthService(auth_repository)
        auth_controller: AuthController = AuthController(auth_service)
        
        return [
            post('/auth/challenge', auth_controller.get_challenge),
            post('/auth/verify', auth_controller.verify_challenge)
        ]