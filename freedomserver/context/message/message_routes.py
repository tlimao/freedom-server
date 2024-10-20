from redis import Redis
from aiohttp.web import RouteDef, get
from freedomlib.message.message_repository import MessageRepository

from freedomserver.context.message.message_controller import MessageController
from freedomserver.context.message.message_service import MessageService

class MessageRoutes:
    
    @classmethod
    def create(cls, message_repository: MessageRepository) -> list[RouteDef]:
        message_service: MessageService = MessageService(message_repository)
        
        message_controller: MessageController = MessageController(message_service)
        
        return [
            get('/ws/message', message_controller.message_handler)
        ]