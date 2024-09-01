import logging
from aiohttp import web
from http import HTTPStatus
from freedomlib.account.account_manager import AccountManager
from freedomlib.account.account_info import AccountInfo
from freedomlib.account.error.account_not_created_error import AccountNotCreatedError
from freedomlib.account.error.account_not_found_error import AccountNotFoundError
from freedomlib.account.account import Account
from freedomlib.key.key_info import KeyInfo
from freedomlib.key.key import Key
from freedomlib.key.key_manager import KeyManager
from freedomserver.context.account.infra.create_account_request import CreateAccountRequest
from freedomserver.context.account.infra.create_account_response import CreateAccountResponse

routes = web.RouteTableDef()

class AccountController:

    def __init__(self, account_manager: AccountManager, key_manager: KeyManager):
        self._account_manager: AccountManager = account_manager
        self._key_manager: KeyManager = key_manager

    async def get_account(self, request: web.Request) -> web.Response:
        try:
            account_id: str = request.match_info['account_id'] 
            
            account: Account = self._account_manager.get_account_by_id(account_id)
            
            return web.json_response(account.to_dict())
        except AccountNotFoundError as e:
            logging.error(e)
            return web.Response(body=str(e), status=HTTPStatus.NOT_FOUND)

    async def create_account(self, request: web.Request) -> web.Response:
        try:
            data: dict = await request.json()
            create_account_request: CreateAccountRequest = CreateAccountRequest.from_dict(data)
            
            # Verifica se a conta já existe
            try:
                existing_account: Account = self._account_manager.get_account_by_phonenumber(create_account_request.account_info.phonenumber)
                # Se a conta existir, retorna a conta existente
                existing_key: Key = self._key_manager.get_account_key(existing_account.id)
                create_account_response: CreateAccountResponse = CreateAccountResponse(
                    account=existing_account,
                    pub_key=existing_key.pub_key
                )
                return web.json_response(create_account_response.to_dict())
            except AccountNotFoundError:
                # Se a conta não existir, cria uma nova
                account: Account = self._account_manager.create_account(create_account_request.account_info)
            
            key_info: KeyInfo = KeyInfo(
                account_id=account.id,
                pub_key=create_account_request.pub_key
            )
            
            key: Key = self._key_manager.put_key(key_info)
            
            create_account_response: CreateAccountResponse = CreateAccountResponse(
                account=account,
                pub_key=key.pub_key
            )

            return web.json_response(create_account_response.to_dict())
        except AccountNotCreatedError as e:
            logging.error(e)
            return web.Response(body=str(e), status=HTTPStatus.BAD_REQUEST)