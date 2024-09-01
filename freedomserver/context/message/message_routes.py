from redis import Redis
from aiohttp.web import RouteDef, get
from freedomlib.message.message_repository import MessageRepository
from freedomlib.message.message_repository_impl import MessageRepositoryImpl
from freedomlib.message.message_manager import MessageManager

from freedomserver.context.message.message_controller import MessageController

class MessageRoutes:
    
    @classmethod
    def create(cls, redis_connection: Redis) -> list[RouteDef]:
        message_repository: MessageRepository = MessageRepositoryImpl(redis_connection)
        message_manager: MessageManager = MessageManager(message_repository)
        
        message_controller: MessageController = MessageController(message_manager)
        
        return [
            get('/ws/message', message_controller.message_handler)
        ]