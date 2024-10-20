import logging
from aiohttp import web
from http import HTTPStatus

from freedomlib.key.key import Key

from freedomserver.context.key.errors.key_error import KeyNotFoundError
from freedomserver.context.key.key_service import KeyService

class KeyController:

    def __init__(self, key_service: KeyService):
        self._key_service: KeyService = key_service

    async def get_key(self, request: web.Request) -> web.Response:
        try:
            aci: str = request.match_info['aci'] 
            
            key: Key = self._key_service.get_key(aci)
            
            return web.json_response(key.to_dict())
        except KeyNotFoundError as e:
            logging.error(e)
            return web.Response(body=str(e), status=HTTPStatus.NOT_FOUND)