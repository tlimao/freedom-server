from aiohttp.web import RouteDef, get
from freedomserver.configuration.server_info_config import ServerInfoConfig
from freedomserver.context.info.info_controller import InfoController

class InfoRoutes:
    
    @classmethod
    def create(cls, server_info: ServerInfoConfig) -> list[RouteDef]:
        info_controller: InfoController = InfoController(server_info)
        
        return [
            get('/info', info_controller.get_info),
            get('/pubkey', info_controller.get_pub_key)
        ]