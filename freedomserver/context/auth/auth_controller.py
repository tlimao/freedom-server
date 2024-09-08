import os
import base64
from aiohttp import web
from freedomserver.context.auth.auth_service import AuthService
from freedomserver.context.server.server_keys import ServerKeys

class AuthController:
    def __init__(self, auth_service: AuthService, server_keys: ServerKeys):
        self._auth_service: AuthService = auth_service
        self._server_keys: ServerKeys = server_keys

    async def get_challenge(self, request: web.Request) -> web.Response:
        data = await request.json()
        account_id: str = data.get('account_id')
        device_id: int = data.get('device_id')
        
        if not account_id or not device_id:
            return web.HTTPBadRequest(reason="ID da conta e ID do dispositivo são obrigatórios")
        
        challenge = base64.b64encode(os.urandom(32)).decode('utf-8')
        self._auth_service.store_challenge(account_id, device_id, challenge)
        return web.json_response({'challenge': challenge })

    async def verify_challenge(self, request: web.Request) -> web.Response:
        data = await request.json()
        account_id = data.get('account_id')
        device_id = data.get('device_id')
        signed_challenge = data.get('signed_challenge')
        client_pub_key = data.get('public_key_to_sign')
        
        if not all([account_id, device_id, signed_challenge, client_pub_key]):
            return web.HTTPBadRequest(reason="Todos os campos são obrigatórios")
        
        try:
            token = self._auth_service.verify_challenge(account_id, device_id, signed_challenge, client_pub_key)
            return web.json_response({'token': token})
        except ValueError as e:
            return web.HTTPUnauthorized(reason=str(e))
