from aiohttp.web import RouteDef, get
from freedomserver.configuration.server_info_config import ServerInfoConfig
from freedomserver.configuration.server_keys import ServerKeys
from freedomserver.context.info.info_controller import InfoController

class InfoRoutes:
    
    @classmethod
    def create(cls, server_info: ServerInfoConfig, server_keys: ServerKeys) -> list[RouteDef]:
        info_controller: InfoController = InfoController(server_info, server_keys)
        
        return [
            get('/info', info_controller.get_info),
            get('/pubkey', info_controller.get_pub_key)
        ]