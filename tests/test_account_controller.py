import json
import pytest
from unittest.mock import MagicMock
from redis import Redis
from fakeredis import FakeRedis
from aiohttp import web

from freedomlib.account.account import Account

from freedomserver.context.account.account_cache import AccountCache
from freedomserver.context.account.account_routes import AccountRoutes
from freedomserver.context.account.dtos.create_account_response import CreateAccountResponse
from freedomserver.context.account.dtos.registration_response import RegistrationResponse
from freedomserver.context.account.errors.account_error import AccountRegistrationError
from freedomserver.context.account.repository.account_repository import AccountRepository
from freedomserver.context.account.repository.account_repository_impl import AccountRepositoryImpl
from freedomserver.context.key.repository.key_repository import KeyRepository
from freedomserver.context.key.repository.key_repository_impl import KeyRepositoryImpl
from freedomserver.context.utils.generate_ids import generate_uuid7_str
from freedomserver.context.utils.mail_sender import MailSender
from tests.commons import ED25519_PUBLIC_KEY, MORTY_EMAIL, MORTY_NICK, MORTY_PHONE, MORTY_PIN_HASH, RICKY_SANCHEZ_ACI, RICKY_SANCHEZ_EMAIL, RICKY_SANCHEZ_NICK, RICKY_SANCHEZ_PHONE, RICKY_SANCHEZ_PIN_HASH, X25519_PUBLIC_KEY

@pytest.fixture
def fake_redis() -> FakeRedis:
    fake_redis: FakeRedis = FakeRedis()
    
    account: Account = Account(
        aci=RICKY_SANCHEZ_ACI,
        nick=RICKY_SANCHEZ_NICK,
        email=RICKY_SANCHEZ_EMAIL,
        phonenumber=RICKY_SANCHEZ_PHONE,
        discoverable=True,
        pin_hash=RICKY_SANCHEZ_PIN_HASH,
    )
    
    fake_redis.set(
        f"account:aci:{account.aci}",
        json.dumps(account.to_dict())
    )
    
    fake_redis.set(
        f"account:e164:{account.phonenumber}",
        account.aci
    )
    
    fake_redis.set(
        f"account:email:{account.email}",
        account.aci
    )
    
    return fake_redis

@pytest.fixture
def account_cache(fake_redis: fake_redis) -> AccountCache:
    return AccountCache(fake_redis)

@pytest.fixture
def account_repository(fake_redis: FakeRedis) -> AccountRepository:
    return AccountRepositoryImpl(fake_redis)

@pytest.fixture
def redis_failure() -> MagicMock:
    redis_failure: MagicMock = MagicMock(spec=Redis)
    
    redis_failure.get.side_effect = AccountRegistrationError()
    
    return redis_failure

@pytest.fixture
def account_repository_failure(redis_failure: FakeRedis) -> AccountRepository:
    return AccountRepositoryImpl(redis_failure)

@pytest.fixture
def mail_sender() -> MagicMock:
    mail_sender: MagicMock = MagicMock(spec=MailSender)
    
    mail_sender.send_email.return_value = True
    
    return mail_sender

@pytest.fixture
def key_repository(fake_redis: FakeRedis) -> KeyRepository:
    return KeyRepositoryImpl(fake_redis)

@pytest.fixture
def mail_sender_fail() -> MagicMock:
    mail_sender: MagicMock = MagicMock(spec=MailSender)
    
    mail_sender.send_email.return_value = False
    
    return mail_sender

async def test_register_new_account(
    aiohttp_client,
    mail_sender: MagicMock,
    account_cache: AccountCache,
    account_repository: AccountRepository,
    key_repository: KeyRepository) -> None:
    
    app = web.Application()
    app.add_routes(AccountRoutes.create(
        mail_sender=mail_sender,
        account_cache=account_cache,
        account_repository=account_repository,
        key_repository=key_repository
    ))
    
    client = await aiohttp_client(app)
    
    registration_request_dict: dict = {
        "email": MORTY_EMAIL,
        "phonenumber": MORTY_PHONE
    }
    
    async with client.post('/account/register', json=registration_request_dict) as resp:
        assert resp.status == 200
        response = await resp.json()
        registration_response: RegistrationResponse = RegistrationResponse.from_dict(response)
        
        assert registration_response.account_lock == False
        assert len(registration_response.request_id) == 6
        assert isinstance(registration_response.request_id, str)

async def test_register_existent_account(
    aiohttp_client,
    mail_sender: MagicMock,
    account_cache: AccountCache,
    account_repository: AccountRepository,
    key_repository: KeyRepository) -> None:
    
    app = web.Application()
    app.add_routes(AccountRoutes.create(
        mail_sender=mail_sender,
        account_cache=account_cache,
        account_repository=account_repository,
        key_repository=key_repository
    ))
    
    client = await aiohttp_client(app)
    
    registration_request_dict: dict = {
        "email": RICKY_SANCHEZ_EMAIL,
        "phonenumber": RICKY_SANCHEZ_PHONE
    }
    
    async with client.post('/account/register', json=registration_request_dict) as resp:
        assert resp.status == 200
        response = await resp.json()
        registration_response = RegistrationResponse(**response)
        
        assert registration_response.account_lock == True
        assert len(registration_response.request_id) == 6
        assert isinstance(registration_response.request_id, str)

async def test_register_account_failed(
    aiohttp_client,
    mail_sender: MagicMock,
    account_cache: AccountCache,
    account_repository_failure: AccountRepository,
    key_repository: KeyRepository) -> None:
    
    app = web.Application()
    app.add_routes(AccountRoutes.create(
        mail_sender=mail_sender,
        account_cache=account_cache,
        account_repository=account_repository_failure,
        key_repository=key_repository
    ))
    
    client = await aiohttp_client(app)
    
    registration_request_dict: dict = {
        "email": "dummy@freedom.mail",
        "phonenumber": RICKY_SANCHEZ_PHONE
    }
    
    async with client.post('/account/register', json=registration_request_dict) as resp:
        assert resp.status == 400
        response = await resp.text()
        
        assert response == "400: Account Registration Failed"
        
async def test_create_new_account_sucess(
    aiohttp_client,
    mail_sender: MagicMock,
    account_cache: AccountCache,
    fake_redis: FakeRedis,
    account_repository: AccountRepository,
    key_repository: KeyRepository) -> None:
    
    app = web.Application()
    app.add_routes(AccountRoutes.create(
        mail_sender=mail_sender,
        account_cache=account_cache,
        account_repository=account_repository,
        key_repository=key_repository
    ))
    
    client = await aiohttp_client(app)
    
    verification_data: dict = {
        "account_lock": False,
        "request_id": "111111"
    }
    
    fake_redis.set(f"account:verification:{MORTY_PHONE}", json.dumps(verification_data))
    
    create_account_request_dict: dict = {
        "request_id": "111111",
        "account_info": {
            "nick": MORTY_NICK,
            "email": MORTY_EMAIL,
            "phonenumber": MORTY_PHONE,
            "ed25519_public_key": ED25519_PUBLIC_KEY,
            "x25519_public_key": X25519_PUBLIC_KEY,
            "discoverable": True,
            "pin_hash": MORTY_PIN_HASH
        }
    }
    
    async with client.post('/account/create', json=create_account_request_dict) as resp:
        assert resp.status == 200
        response = await resp.json()
        create_account_response: CreateAccountResponse = CreateAccountResponse.from_dict(response)
        
        assert create_account_response.account_data.discoverable == True
        assert create_account_response.account_data.ed25519_public_key == ED25519_PUBLIC_KEY
        assert create_account_response.account_data.x25519_public_key == X25519_PUBLIC_KEY
        assert create_account_response.account_data.email == MORTY_EMAIL
        assert create_account_response.account_data.phonenumber == MORTY_PHONE
    
async def test_create_existent_account_success(
    aiohttp_client,
    mail_sender: MagicMock,
    account_cache: AccountCache,
    fake_redis: FakeRedis,
    account_repository: AccountRepository,
    key_repository: KeyRepository) -> None:
    
    app = web.Application()
    app.add_routes(AccountRoutes.create(
        mail_sender=mail_sender,
        account_cache=account_cache,
        account_repository=account_repository,
        key_repository=key_repository
    ))
    
    client = await aiohttp_client(app)
    
    verification_data: dict = {
        "account_lock": True,
        "request_id": "111111"
    }
    
    fake_redis.set(f"account:verification:{RICKY_SANCHEZ_PHONE}", json.dumps(verification_data))
    
    create_account_request_dict: dict = {
        "request_id": "111111",
        "account_info": {
            "nick": RICKY_SANCHEZ_NICK,
            "email": RICKY_SANCHEZ_EMAIL,
            "phonenumber": RICKY_SANCHEZ_PHONE,
            "ed25519_public_key": ED25519_PUBLIC_KEY,
            "x25519_public_key": X25519_PUBLIC_KEY,
            "discoverable": True,
            "pin_hash": RICKY_SANCHEZ_PIN_HASH
        }
    }
    
    async with client.post('/account/create', json=create_account_request_dict) as resp:
        assert resp.status == 200
        response = await resp.json()
        create_account_response: CreateAccountResponse = CreateAccountResponse.from_dict(response)
        
        assert create_account_response.account_data.discoverable == True
        assert create_account_response.account_data.ed25519_public_key == ED25519_PUBLIC_KEY
        assert create_account_response.account_data.x25519_public_key == X25519_PUBLIC_KEY
        assert create_account_response.account_data.email == RICKY_SANCHEZ_EMAIL
        assert create_account_response.account_data.phonenumber == RICKY_SANCHEZ_PHONE 

async def test_create_existent_account_failure_invalid_pin(
    aiohttp_client,
    mail_sender: MagicMock,
    account_cache: AccountCache,
    fake_redis: FakeRedis,
    account_repository: AccountRepository,
    key_repository: KeyRepository) -> None:
    
    app = web.Application()
    app.add_routes(AccountRoutes.create(
        mail_sender=mail_sender,
        account_cache=account_cache,
        account_repository=account_repository,
        key_repository=key_repository
    ))
    
    client = await aiohttp_client(app)
    
    verification_data: dict = {
        "account_lock": True,
        "request_id": "111111"
    }
    
    fake_redis.set(f"account:verification:{RICKY_SANCHEZ_PHONE}", json.dumps(verification_data))
    
    create_account_request_dict: dict = {
        "request_id": "111111",
        "account_info": {
            "nick": RICKY_SANCHEZ_NICK,
            "email": RICKY_SANCHEZ_EMAIL,
            "phonenumber": RICKY_SANCHEZ_PHONE,
            "ed25519_public_key": ED25519_PUBLIC_KEY,
            "x25519_public_key": X25519_PUBLIC_KEY,
            "discoverable": True,
            "pin_hash": "invalid_pin_hash"
        }
    }
    
    async with client.post('/account/create', json=create_account_request_dict) as resp:
        assert resp.status == 400
        response = await resp.text()
        
        assert response == "400: Incorrect PIN!"