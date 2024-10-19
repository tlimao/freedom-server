import redis

from aiohttp.web import Application

from freedomserver.context.account.account_routes import AccountRoutes
from freedomserver.context.utils.mail_sender import MailSender
from freedomserver.server_config import ServerConfig
from freedomserver.context.info.info_routes import InfoRoutes
class ServerRoutes:
    
    @classmethod
    def setup_routes(cls, app: Application, config: ServerConfig) -> None:
        redis_connection: redis.Redis = redis.Redis(
            host=config.redis_config.host,
            port=config.redis_config.port
        )
        
        mail_sender: MailSender = MailSender(config.smtp_config)
        # sms_sender: SmsSender = SmsSender()
        
        app.add_routes(AccountRoutes.create(mail_sender, redis_connection))
        # app.add_routes(MessageRoutes.create(redis_connection))
        app.add_routes(InfoRoutes.create(config.server_info, config.server_keys))
        
        