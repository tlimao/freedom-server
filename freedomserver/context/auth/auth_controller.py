import logging
from aiohttp import web
from freedomserver.context.auth.auth_service import AuthService
from freedomserver.context.auth.dtos.auth_challenge_request import AuthChallengeRequest
from freedomserver.context.auth.dtos.auth_challenge import AuthChallenge
from freedomserver.context.auth.dtos.auth_challenge_response import AuthChallengeResponse
from freedomserver.context.auth.dtos.auth_verify import AuthVerify
from freedomserver.context.auth.dtos.auth_verify_request import AuthVerifyRequest
from freedomserver.context.auth.dtos.auth_verify_response import AuthVerifyResponse

class AuthController:

    def __init__(self, auth_service: AuthService):
        self._auth_service: AuthService = auth_service

    async def challenge(self, request: web.Request) -> web.Response:
        try:
            auth_challenge_request: AuthChallengeRequest = AuthChallengeRequest.from_dict(await request.json())
            
            auth_challenge: AuthChallenge = self._auth_service.get_challenge(
                auth_challenge_request.aci,
                auth_challenge_request.device_id
            )
            
            auth_challenge_response: AuthChallengeResponse = AuthChallengeResponse(**auth_challenge)
            
            return web.json_response(auth_challenge_response.to_dict())
        except Exception as e:
            logging.error(e)
            return web.HTTPBadRequest(reason="Invalid Request")

    async def verify(self, request: web.Request) -> web.Response:
        try:
            auth_verify_request: AuthVerifyRequest = AuthVerifyRequest.from_dict(await request.json())
            
            auth_verify: AuthVerify = self._auth_service.verify_challenge(
                auth_verify_request.aci,
                auth_verify_request.device_id,
                auth_verify_request.challenge,
                auth_verify_request.signature)
            
            auth_verify_response: AuthVerifyResponse = AuthVerifyResponse(**auth_verify)
            
            return web.json_response(auth_verify_response.to_dict())
        except ValueError as e:
            return web.HTTPUnauthorized(reason=str(e))
