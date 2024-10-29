from aiohttp.web import RouteDef, get

from freedomserver.configuration.server_keys import ServerKeys
from freedomserver.context.auth.auth_service import AuthService
from freedomserver.context.auth.repository.auth_repository import AuthRepository
from freedomserver.context.key.repository.key_repository import KeyRepository
from freedomserver.context.message.message_controller import MessageController
from freedomserver.context.message.message_repository import MessageRepository
from freedomserver.context.message.message_service import MessageService

class MessageRoutes:
    
    @classmethod
    def create(cls,
               server_keys: ServerKeys,
               message_repository: MessageRepository,
               auth_repository: AuthRepository,
               key_repository: KeyRepository) -> list[RouteDef]:
        
        message_service: MessageService = MessageService(message_repository)
        auth_service: AuthService = AuthService(server_keys, auth_repository, key_repository)
        
        message_controller: MessageController = MessageController(message_service, auth_service)
        
        return [
            get('/ws/message', message_controller.message_handler)
        ]