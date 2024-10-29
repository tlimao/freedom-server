import redis

from aiohttp.web import Application

from freedomserver.configuration.server_keys import ServerKeys
from freedomserver.context.account.account_cache import AccountCache
from freedomserver.context.account.account_routes import AccountRoutes
from freedomserver.context.account.repository.account_repository import AccountRepository
from freedomserver.context.account.repository.account_repository_impl import AccountRepositoryImpl
from freedomserver.context.auth.auth_routes import AuthRoutes
from freedomserver.context.auth.repository.auth_repository import AuthRepository
from freedomserver.context.auth.repository.auth_repository_impl import AuthRepositoryImpl
from freedomserver.context.contact.contact_routes import ContactRoutes
from freedomserver.context.key.repository.key_repository import KeyRepository
from freedomserver.context.key.repository.key_repository_impl import KeyRepositoryImpl
from freedomserver.context.key.key_routes import KeyRoutes
from freedomserver.context.message.message_repository import MessageRepository
from freedomserver.context.message.message_repository_impl import MessageRepositoryImpl
from freedomserver.context.message.message_routes import MessageRoutes
from freedomserver.context.utils.mail_sender import MailSender
from freedomserver.server_config import ServerConfig
from freedomserver.context.info.info_routes import InfoRoutes
class ServerRoutes:
    
    @classmethod
    def setup_routes(cls, app: Application, config: ServerConfig) -> None:
        server_keys: ServerKeys = config.server_keys
        
        redis_connection: redis.Redis = redis.Redis(
            host=config.redis_config.host,
            port=config.redis_config.port
        )
        
        mail_sender: MailSender = MailSender(config.smtp_config)
        # sms_sender: SmsSender = SmsSender()
        
        # Repositories
        account_repository: AccountRepository = AccountRepositoryImpl(redis_connection)
                
        key_repository: KeyRepository = KeyRepositoryImpl(redis_connection)
        
        account_cache: AccountCache = AccountCache(redis_connection)
        
        auth_repository: AuthRepository = AuthRepositoryImpl(redis_connection)
        
        message_repository: MessageRepository = MessageRepositoryImpl(redis_connection)
        
        app.add_routes(AccountRoutes.create(
            mail_sender,
            account_repository,
            account_cache,
            key_repository))
        app.add_routes(KeyRoutes.create(
            key_repository))
        app.add_routes(InfoRoutes.create(
            config.server_info,
            config.server_keys))
        app.add_routes(ContactRoutes.create(
            account_repository,
            key_repository))
        app.add_routes(MessageRoutes.create(
            server_keys,
            message_repository,
            auth_repository,
            key_repository))
        app.add_routes(AuthRoutes.create(
            server_keys,
            auth_repository,
            key_repository))
        
        