import os
from aiohttp import web
from freedomserver.context.auth.auth_service import AuthService

class AuthController:
    def __init__(self, auth_service: AuthService):
        self._auth_service: AuthService = auth_service

    async def get_challenge(self, request: web.Request) -> web.Response:
        data = await request.json()
        account_id: str = data.get('account_id')
        device_id: int = data.get('device_id')
        # signature: str = data.get('signature')
        
        if not account_id or not device_id:
            return web.HTTPBadRequest(reason="ID da conta e ID do dispositivo são obrigatórios")
        
        challenge = os.urandom(32).hex()
        await self._auth_service.store_challenge(account_id, device_id, challenge)
        return web.json_response({'challenge': challenge})

    async def verify_challenge(self, request: web.Request) -> web.Response:
        data = await request.json()
        account_id = data.get('account_id')
        device_id = data.get('device_id')
        signed_challenge = data.get('signed_challenge')
        
        if not all([account_id, device_id, signed_challenge]):
            return web.HTTPBadRequest(reason="Todos os campos são obrigatórios")
        
        try:
            token = await self._auth_service.verify_challenge(account_id, device_id, signed_challenge)
            return web.json_response({'token': token})
        except ValueError as e:
            return web.HTTPUnauthorized(reason=str(e))
