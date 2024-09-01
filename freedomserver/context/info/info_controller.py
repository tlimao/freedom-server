from aiohttp.web import Request, Response, json_response
from freedomserver.configuration.server_info_config import ServerInfoConfig

class InfoController:
    
    def __init__(self, server_info: ServerInfoConfig) -> None:
        self._server_info: ServerInfoConfig = server_info

    async def get_info(self, request: Request) -> Response:
        return json_response(self._server_info.to_dict())