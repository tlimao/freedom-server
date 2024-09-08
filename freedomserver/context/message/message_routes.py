from redis import Redis
from aiohttp.web import RouteDef, get
from freedomlib.message.message_repository import MessageRepository
from freedomlib.message.message_repository_impl import MessageRepositoryImpl
from freedomlib.message.message_manager import MessageManager
from freedomserver.context.message.message_service import MessageService
from freedomserver.context.auth.auth_service import AuthService
from freedomserver.context.auth.auth_repository import AuthRepository
from freedomserver.context.auth.auth_repository_impl import AuthRepositoryImpl
from freedomserver.context.message.message_controller import MessageController
from freedomlib.key.key_repository import KeyRepository
from freedomlib.key.key_repository_impl import KeyRepositoryImpl
from freedomlib.key.key_manager import KeyManager
from freedomserver.context.server.server_keys import ServerKeys

class MessageRoutes:
    
    @classmethod
    def create(cls, redis_connection: Redis, server_keys: ServerKeys) -> list[RouteDef]:
        message_repository: MessageRepository = MessageRepositoryImpl(redis_connection)
        message_service: MessageService = MessageService(message_repository)

        key_repository: KeyRepository = KeyRepositoryImpl(redis_connection)
        key_manager: KeyManager = KeyManager(key_repository)

        auth_repository: AuthRepository = AuthRepositoryImpl(redis_connection)
        auth_service: AuthService = AuthService(auth_repository, key_manager)
        
        message_controller: MessageController = MessageController(message_service, auth_service, server_keys)

        return [
            get('/ws/message', message_controller.message_handler)
        ]