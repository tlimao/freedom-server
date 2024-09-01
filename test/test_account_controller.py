from freedomlib.account.account import Account
from freedomlib.account.account_info import AccountInfo
from freedomserver.context.account.infra.create_account_request import CreateAccountRequest
from freedomserver.context.account.infra.create_account_response import CreateAccountResponse
from freedomserver.context.account.account_routes import AccountRoutes
from fakeredis import FakeRedis
from aiohttp import web
import pytest

@pytest.fixture
def fake_redis():
    # Cria uma conexão fake do Redis usando fakeredis
    return FakeRedis()

async def test_create_new_account(aiohttp_client, fake_redis: FakeRedis):
    account_info: AccountInfo = AccountInfo(nick="@account1", email="account1@mail.com", phonenumber="1234567890")
    pub_key: str = "------------- BEGIN KEY ------------- ... ----------- END KEY -----------"

    create_account_request: CreateAccountRequest = CreateAccountRequest(account_info=account_info, pub_key=pub_key)
    
    app = web.Application()
    app.add_routes(AccountRoutes.create(fake_redis))
    
    client = await aiohttp_client(app)
    
    async with client.post('/account', json=create_account_request.to_dict()) as resp:
        assert resp.status == 200
        response = await resp.json()
        create_account_response = CreateAccountResponse(
            account=Account(**response['account']),
            pub_key=response['pub_key']
        )
        
        assert create_account_response.account.nick == account_info.nick
        assert create_account_response.account.email == account_info.email
        assert create_account_response.account.phonenumber == account_info.phonenumber
        assert create_account_response.pub_key == pub_key
        
    async with client.get(f'/account/{create_account_response.account.id}') as resp:
        assert resp.status == 200
        response = await resp.json()
        account = Account(**response)
        
        assert account.nick == account_info.nick
        assert account.email == account_info.email
        assert account.phonenumber == account_info.phonenumber

async def test_create_existing_account(aiohttp_client, fake_redis: FakeRedis):
    account_info: AccountInfo = AccountInfo(nick="@account1", email="account1@mail.com", phonenumber="1234567890")
    pub_key: str = "------------- BEGIN KEY ------------- ... ----------- END KEY -----------"

    create_account_request: CreateAccountRequest = CreateAccountRequest(account_info=account_info, pub_key=pub_key)
    
    app = web.Application()
    app.add_routes(AccountRoutes.create(fake_redis))
    
    client = await aiohttp_client(app)
    
    async with client.post('/account', json=create_account_request.to_dict()) as resp:
        assert resp.status == 200
        response = await resp.json()
        create_account_response = CreateAccountResponse(
            account=Account(**response['account']),
            pub_key=response['pub_key']
        )
        
        assert create_account_response.account.nick == account_info.nick
        assert create_account_response.account.email == account_info.email
        assert create_account_response.account.phonenumber == account_info.phonenumber
        assert create_account_response.pub_key == pub_key
        
    async with client.post('/account', json=create_account_request.to_dict()) as resp:
        assert resp.status == 200
        response = await resp.json()
        create_account_response = CreateAccountResponse(
            account=Account(**response['account']),
            pub_key=response['pub_key']
        )
        
        assert create_account_response.account.nick == account_info.nick
        assert create_account_response.account.email == account_info.email
        assert create_account_response.account.phonenumber == account_info.phonenumber
        assert create_account_response.pub_key == pub_key