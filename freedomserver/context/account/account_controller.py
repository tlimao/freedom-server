import logging
from aiohttp import web
from freedomserver.context.account.dtos.account_registration import AccountRegistration
from freedomserver.context.account.dtos.registration_request import RegistrationRequest
from freedomserver.context.account.dtos.registration_response import RegistrationResponse
from freedomserver.context.account.account_service import AccountService
from freedomserver.context.account.errors.account_error import AccountRegistrationError

class AccountController:

    def __init__(self, account_service: AccountService):
        self._account_service: AccountService = account_service

    async def register(self, request: web.Request) -> web.Response:
        try:
            registration_request: RegistrationRequest = RegistrationRequest.from_dict(await request.json())
            
            account_registration: AccountRegistration = self._account_service.register_account(
                registration_request.phonenumber, registration_request.email
            )
            
            registration_response: RegistrationResponse = RegistrationResponse(
                registration_id=account_registration.registration_id,
                account_lock=account_registration.account_lock
            )
            
            return web.json_response(registration_response.to_dict())
        
        except AccountRegistrationError as e:
            logging.error(e)
            return web.Response(status=500, body=str(e))

    async def verify(self, request: web.Request) -> web.Response:
        ...
        
    async def get_account(self, request: web.Request) -> web.Response:
        ...

    async def create(self, request: web.Request) -> web.Response:
        ...

    async def profile(self, request: web.Request) -> web.Response:
        ...

    async def update_profile(self, request: web.Request) -> web.Response:
        ...

    async def update_privacy(self, request: web.Request) -> web.Response:
        ...
