import logging
from aiohttp import web
from http import HTTPStatus
from freedomlib.account.error.account_not_created_error import AccountNotCreatedError
from freedomlib.account.error.account_not_found_error import AccountNotFoundError
from freedomlib.account.account import Account
from freedomserver.context.account.infra.create_account import CreateAccountRequest
from freedomserver.context.account.infra.create_account import CreateAccountResponse
from freedomserver.context.account.account_service import AccountService

class AccountController:

    def __init__(self, account_service: AccountService):
        self._account_service: AccountService = account_service

    async def get_account(self, request: web.Request) -> web.Response:
        try:
            account_id: str = request.match_info['account_id'] 
            
            account: Account = self._account_service.get_account(account_id)
            
            return web.json_response(account.to_dict())
        except AccountNotFoundError as e:
            logging.error(e)
            return web.Response(body=str(e), status=HTTPStatus.NOT_FOUND)

    async def create_account(self, request: web.Request) -> web.Response:
        try:
            data: dict = await request.json()
            create_account_request: CreateAccountRequest = CreateAccountRequest.from_dict(data)
            
            account, account_key = self._account_service.create_account(
                create_account_request.account_info, create_account_request.pub_key)
            
            create_account_response: CreateAccountResponse = CreateAccountResponse(
                account=account, pub_key=account_key.pub_key)

            return web.json_response(create_account_response.to_dict())
        except AccountNotCreatedError as e:
            logging.error(e)
            return web.Response(body=str(e), status=HTTPStatus.BAD_REQUEST)