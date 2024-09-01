import logging
from aiohttp import web
from http import HTTPStatus

from freedomlib.key.error.key_not_found_error import KeyNotFoundError
from freedomlib.key.key_manager import KeyManager
from freedomlib.key.key import Key

routes = web.RouteTableDef()

class KeyController:

    def __init__(self, key_manager: KeyManager):
        self._key_manager: KeyManager = key_manager

    async def get_account_key(self, request: web.Request) -> web.Response:
        try:
            account_id: str = request.match_info['account_id'] 
            
            key: Key = self._key_manager.get_account_key(account_id)
            
            return web.json_response(key.to_dict())
        except KeyNotFoundError as e:
            logging.error(e)
            return web.Response(body=str(e), status=HTTPStatus.NOT_FOUND)