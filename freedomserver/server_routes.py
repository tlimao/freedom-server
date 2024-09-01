import redis

from aiohttp.web import Application

from freedomserver.context.account.account_routes import AccountRoutes
from freedomserver.context.message.message_routes import MessageRoutes

class ServerRoutes:
    
    @classmethod
    def setup_routes(cls, app: Application) -> None:
        redis_connection: redis.Redis = redis.Redis()
        
        app.add_routes(AccountRoutes.create(redis_connection))
        app.add_routes(MessageRoutes.create(redis_connection))
        
        