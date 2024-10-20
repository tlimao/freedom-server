import os
from aiohttp import web
from freedomserver.context.auth.auth_service import AuthService

class AuthController:

    def __init__(self, auth_service: AuthService):
        self._auth_service: AuthService = auth_service

    async def challenge(self, request: web.Request) -> web.Response:
        data = await request.json()
        aci: str = data.get('aci')
        did: int = data.get('did')
        # signature: str = data.get('signature')
        
        if not aci or not did:
            return web.HTTPBadRequest(reason="ID da conta e ID do dispositivo são obrigatórios")
        
        challenge = os.urandom(32).hex()
        self._auth_service.store_challenge(aci, did, challenge)
        return web.json_response({'challenge': challenge})

    async def verify(self, request: web.Request) -> web.Response:
        data = await request.json()
        aci = data.get('aci')
        did = data.get('did')
        signed_challenge = data.get('signed_challenge')
        
        if not all([aci, did, signed_challenge]):
            return web.HTTPBadRequest(reason="Todos os campos são obrigatórios")
        
        try:
            token = self._auth_service.verify_challenge(aci, did, signed_challenge)
            return web.json_response({'token': token})
        except ValueError as e:
            return web.HTTPUnauthorized(reason=str(e))
