import json
from freedomlib.account.account import Account
from redis import Redis
from freedomserver.context.account.account_routes import AccountRoutes
from fakeredis import FakeRedis
from aiohttp import web
import pytest
from unittest.mock import MagicMock

from freedomserver.context.account.dtos.registration_request import RegistrationRequest
from freedomserver.context.account.dtos.registration_response import RegistrationResponse
from freedomserver.context.account.errors.account_error import AccountRegistrationError
from freedomserver.context.utils.generate_ids import generate_uuid7_str
from freedomserver.context.utils.mail_sender import MailSender

@pytest.fixture
def fake_redis() -> FakeRedis:
    fake_redis: FakeRedis = FakeRedis()
    
    existent_account: Account = Account(
        aci=generate_uuid7_str(),
        nick="existent account",
        email="existent@freedom.mail",
        phonenumber="+5577999999999",
        discoverable=True,
        pin_hash="dummy_hash",
    )
    
    fake_redis.set(
        f"account:aci:{existent_account.aci}",
        json.dumps(existent_account.to_dict())
    )
    
    fake_redis.set(
        f"account:e164:{existent_account.phonenumber}",
        existent_account.aci
    )
    
    fake_redis.set(
        f"account:email:{existent_account.email}",
        existent_account.aci
    )
    
    return fake_redis

@pytest.fixture
def redis_failure() -> MagicMock:
    redis_failure: MagicMock = MagicMock(spec=Redis)
    
    redis_failure.get.side_effect = AccountRegistrationError()
    
    return redis_failure

@pytest.fixture
def mail_sender() -> MagicMock:
    mail_sender: MagicMock = MagicMock(spec=MailSender)
    
    mail_sender.send_email.return_value = True
    
    return mail_sender

@pytest.fixture
def mail_sender_fail() -> MagicMock:
    mail_sender: MagicMock = MagicMock(spec=MailSender)
    
    mail_sender.send_email.return_value = False
    
    return mail_sender

async def test_register_new_account(aiohttp_client, fake_redis: FakeRedis, mail_sender: MagicMock) -> None:
    app = web.Application()
    app.add_routes(AccountRoutes.create(mail_sender, fake_redis))
    
    client = await aiohttp_client(app)
    
    registration_request_dict: dict = {
        "email": "dummy@test.mail",
        "phonenumber": "+5566999999999"
    }
    
    async with client.post('/account/register', json=registration_request_dict) as resp:
        assert resp.status == 200
        response = await resp.json()
        registration_response = RegistrationResponse(**response)
        
        assert registration_response.account_lock == False
        assert len(registration_response.registration_id) == 6
        assert isinstance(registration_response.registration_id, str)

async def test_register_existent_account(aiohttp_client, fake_redis: FakeRedis, mail_sender: MagicMock) -> None:
    app = web.Application()
    app.add_routes(AccountRoutes.create(mail_sender, fake_redis))
    
    client = await aiohttp_client(app)
    
    registration_request_dict: dict = {
        "email": "dummy@test.mail",
        "phonenumber": "+5577999999999"
    }
    
    async with client.post('/account/register', json=registration_request_dict) as resp:
        assert resp.status == 200
        response = await resp.json()
        registration_response = RegistrationResponse(**response)
        
        assert registration_response.account_lock == True
        assert len(registration_response.registration_id) == 6
        assert isinstance(registration_response.registration_id, str)

async def test_register_account_failed(aiohttp_client, redis_failure: FakeRedis, mail_sender: MagicMock) -> None:
    app = web.Application()
    app.add_routes(AccountRoutes.create(mail_sender, redis_failure))
    
    client = await aiohttp_client(app)
    
    registration_request_dict: dict = {
        "email": "dummy@test.mail",
        "phonenumber": "+5566999999999"
    }
    
    async with client.post('/account/register', json=registration_request_dict) as resp:
        assert resp.status == 500
        response = await resp.text()
        
        assert response == "Account Registration Failed"