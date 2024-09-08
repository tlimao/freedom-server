import redis

from aiohttp.web import Application

from freedomserver.context.account.account_routes import AccountRoutes
from freedomserver.context.message.message_routes import MessageRoutes
from freedomserver.context.key.key_routes import KeyRoutes
from freedomserver.server_config import ServerConfig
from freedomserver.context.info.info_routes import InfoRoutes
from freedomserver.context.server.server_keys import ServerKeys
from freedomserver.configuration.server_info_config import ServerInfoConfig
from freedomserver.context.auth.auth_routes import AuthRoutes
from freedomserver.context.contact.contact_routes import ContactRoutes

class ServerRoutes:
    
    @classmethod
    def setup_routes(cls, app: Application, config: ServerConfig) -> None:
        redis_connection: redis.Redis = redis.Redis(
            host=config.get_redis_config().host,
            port=config.get_redis_config().port
        )
        
        server_keys: ServerKeys = config.get_server_keys()
        server_info: ServerInfoConfig = config.get_server_info()
        
        app.add_routes(AuthRoutes.create(redis_connection, server_keys))
        app.add_routes(AccountRoutes.create(redis_connection))
        app.add_routes(MessageRoutes.create(redis_connection, server_keys))
        app.add_routes(KeyRoutes.create(redis_connection))
        app.add_routes(InfoRoutes.create(server_info))
        app.add_routes(ContactRoutes.create(redis_connection))
        
        