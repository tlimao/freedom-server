from aiohttp.web import Request, Response, json_response
from freedomserver.configuration.server_info_config import ServerInfoConfig
from freedomserver.configuration.server_keys import ServerKeys

class InfoController:
    
    def __init__(self, server_info: ServerInfoConfig, server_keys: ServerKeys) -> None:
        self._server_info: ServerInfoConfig = server_info
        self._server_keys: ServerKeys = server_keys

    async def get_info(self, request: Request) -> Response:
        return json_response(self._server_info.to_dict())

    async def get_pub_key(self, request: Request) -> Response:
        return json_response({
            "serve_public_key": self._server_keys.public_key()
        })