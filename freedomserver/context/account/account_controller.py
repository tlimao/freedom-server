import logging
from aiohttp import web
from freedomserver.context.account.dtos.account_data import AccountData
from freedomserver.context.account.dtos.account_info import AccountInfo
from freedomserver.context.account.dtos.account_profile import AccountProfile
from freedomserver.context.account.dtos.account_registration import AccountRegistration
from freedomserver.context.account.dtos.account_verification import AccountVerification
from freedomserver.context.account.dtos.create_account_request import CreateAccountRequest
from freedomserver.context.account.dtos.create_account_response import CreateAccountResponse
from freedomserver.context.account.dtos.registration_request import RegistrationRequest
from freedomserver.context.account.dtos.registration_response import RegistrationResponse
from freedomserver.context.account.account_service import AccountService
from freedomserver.context.account.dtos.update_profile_request import UpdateProfileRequest
from freedomserver.context.account.dtos.update_profile_response import UpdateProfileResponse
from freedomserver.context.account.dtos.verification_request import VerificationRequest
from freedomserver.context.account.dtos.verification_response import VerificationResponse
from freedomserver.context.account.errors.account_error import AccountNotCreatedError, AccountNotFoundError, AccountRegistrationError, AccountUpdateError, AccountVerificationError

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
                request_id=account_registration.request_id,
                account_lock=account_registration.account_lock
            )
            
            return web.json_response(registration_response.to_dict())
        
        except AccountRegistrationError as e:
            logging.error(e)
            return web.Response(status=500, body=str(e))

    async def verify(self, request: web.Request) -> web.Response:
        try:
            verification_request: VerificationRequest = VerificationRequest.from_dict(await request.json())
            
            account_verification: AccountVerification = self._account_service.verify_account(
                verification_request.request_id, 
                verification_request.verification_code, 
                verification_request.phonenumber
            )
            
            verification_response: VerificationResponse = VerificationResponse(
                verification_id=account_verification.verification_id,
                account_lock=account_verification.account_lock
            )
            
            return web.json_response(verification_response.to_dict())
        
        except AccountVerificationError as e:
            logging.error(e)
            return web.Response(status=500, body=str(e))

    async def create(self, request: web.Request) -> web.Response:
        try:
            create_account_request: CreateAccountRequest = CreateAccountRequest.from_dict(await request.json())
            
            account_info: AccountInfo = create_account_request.account_info
            request_id: str = create_account_request.request_id
            
            account_data: AccountData = self._account_service.create_account(request_id, account_info)
            
            create_account_response: CreateAccountResponse = CreateAccountResponse(
                account_data=account_data
            )
            
            return web.json_response(create_account_response.to_dict())
            
        except AccountNotCreatedError as e:
            logging.error(e)
            return web.Response(status=500, body=str(e))

    async def get_profile(self, request: web.Request) -> web.Response:
        try:
            aci: str = request.match_info.get('aci')
            
            account_profile: AccountProfile = self._account_service.get_profile(aci)
            
            return web.json_response(account_profile.to_dict())
            
        except AccountNotFoundError as e:
            logging.error(e)
            return web.Response(status=500, body=str(e))

    async def update_profile(self, request: web.Request) -> web.Response:
        try:
            update_profile_request: UpdateProfileRequest = UpdateProfileRequest.from_dict(await request.json())
            
            account_profile: AccountProfile = self._account_service.update_profile(
                update_profile_request.account_profile
            )
            
            update_profile_response: UpdateProfileResponse = UpdateProfileResponse(
                account_profile=account_profile
            )
            
            return web.json_response(update_profile_response.to_dict())
            
        except AccountUpdateError as e:
            logging.error(e)
            return web.Response(status=500, body=str(e))
