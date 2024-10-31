
import pytest

from fakeredis import FakeRedis
from aiohttp import web

from freedomlib.crypto.functions import ED25519
from freedomlib.utils.serializable import Serializable
from freedomlib.key.key_box import KeyBox

from freedomserver.configuration.server_keys import ServerKeys
from freedomserver.context.auth.auth_routes import AuthRoutes
from freedomserver.context.auth.dtos.auth_challenge_response import AuthChallengeResponse
from freedomserver.context.auth.dtos.auth_verify_request import AuthVerifyRequest
from freedomserver.context.auth.repository.auth_repository import AuthRepository
from freedomserver.context.auth.repository.auth_repository_impl import AuthRepositoryImpl
from freedomserver.context.key.repository.key_repository import KeyRepository
from freedomserver.context.key.repository.key_repository_impl import KeyRepositoryImpl
from tests.commons import ED25519_PRIVATE_KEY, ED25519_PUBLIC_KEY, RICKY_SANCHEZ_ACI, SERVER_PRIVATE_KEY, SERVER_PUBLIC_KEY, X25519_PUBLIC_KEY


@pytest.fixture
def fake_redis() -> FakeRedis:
    return FakeRedis()

@pytest.fixture
def auth_repository(fake_redis) -> AuthRepository:
    return AuthRepositoryImpl(fake_redis)

@pytest.fixture
def key_repository(fake_redis) -> KeyRepository:
    return KeyRepositoryImpl(fake_redis)

@pytest.fixture
def server_keys() -> ServerKeys:
    return ServerKeys(
        private_key=SERVER_PRIVATE_KEY,
        public_key=SERVER_PUBLIC_KEY
    )

async def test_account_request_challenge(
    aiohttp_client,
    auth_repository: AuthRepository,
    key_repository: KeyRepository,
    server_keys: ServerKeys) -> None:

    app = web.Application()
    app.add_routes(AuthRoutes.create(
        key_repository=key_repository,
        auth_repository=auth_repository,
        server_keys=server_keys
    ))
    
    client = await aiohttp_client(app)
    
    challenge_request_dict: dict = {
        "aci": RICKY_SANCHEZ_ACI,
        "device_id": "1"
    }
    
    async with client.post('/auth/challenge', json=challenge_request_dict) as resp:
        assert resp.status == 200
        response = await resp.json()
        
        auth_challenge_response: AuthChallengeResponse = AuthChallengeResponse.from_dict(response)
        
        ED25519.verify(
            server_keys.get_public_key(),
            Serializable.b64_str_to_bytes(auth_challenge_response.signature),
            Serializable.str_to_bytes(f"{auth_challenge_response.request_id}:{auth_challenge_response.challenge}"))

async def test_account_request_verify(
    aiohttp_client,
    auth_repository: AuthRepository,
    key_repository: KeyRepository,
    server_keys: ServerKeys) -> None:
    
    key_box: KeyBox = KeyBox(
        aci=RICKY_SANCHEZ_ACI,
        id="ricky_sanchez_key_id",
        ed25519_public_key=ED25519_PUBLIC_KEY,
        x25519_public_key=X25519_PUBLIC_KEY
    )
    
    key_repository.save(key_box)

    app = web.Application()

    app.add_routes(AuthRoutes.create(
        key_repository=key_repository,
        auth_repository=auth_repository,
        server_keys=server_keys
    ))
    
    client = await aiohttp_client(app)
    
    challenge_request_dict: dict = {
        "aci": RICKY_SANCHEZ_ACI,
        "device_id": "1"
    }
    
    async with client.post('/auth/challenge', json=challenge_request_dict) as resp:
        assert resp.status == 200
        response = await resp.json()
        
        auth_challenge_response: AuthChallengeResponse = AuthChallengeResponse.from_dict(response)
        
    auth_verify_request: AuthVerifyRequest = AuthVerifyRequest(
        aci=RICKY_SANCHEZ_ACI,
        challenge=auth_challenge_response.challenge,
        device_id="1",
        request_id=auth_challenge_response.request_id,
        signature=Serializable.bytes_to_b64_str(ED25519.sign(
            ED25519.load_private_key_from_pem(ED25519_PRIVATE_KEY),
            Serializable.str_to_bytes(auth_challenge_response.challenge))
        )
    )
        
    async with client.post('/auth/verify', json=auth_verify_request.to_dict()) as resp:
        assert resp.status == 200
        response = await resp.json()
        
        assert response.get('token') != ''

async def test_account_request_invalid_verify(
    aiohttp_client,
    auth_repository: AuthRepository,
    key_repository: KeyRepository,
    server_keys: ServerKeys) -> None:
    
    key_box: KeyBox = KeyBox(
        aci=RICKY_SANCHEZ_ACI,
        id="ricky_sanchez_key_id",
        ed25519_public_key=ED25519_PUBLIC_KEY,
        x25519_public_key=X25519_PUBLIC_KEY
    )
    
    key_repository.save(key_box)

    app = web.Application()

    app.add_routes(AuthRoutes.create(
        key_repository=key_repository,
        auth_repository=auth_repository,
        server_keys=server_keys
    ))
    
    client = await aiohttp_client(app)
    
    challenge_request_dict: dict = {
        "aci": RICKY_SANCHEZ_ACI,
        "device_id": "1"
    }
    
    async with client.post('/auth/challenge', json=challenge_request_dict) as resp:
        assert resp.status == 200
        response = await resp.json()
        
        auth_challenge_response: AuthChallengeResponse = AuthChallengeResponse.from_dict(response)
        
    auth_verify_request: AuthVerifyRequest = AuthVerifyRequest(
        aci=RICKY_SANCHEZ_ACI,
        challenge=auth_challenge_response.challenge,
        device_id="1",
        request_id=auth_challenge_response.request_id,
        signature="invalid_signature"
    )
        
    async with client.post('/auth/verify', json=auth_verify_request.to_dict()) as resp:
        assert resp.status == 401

        response = await resp.text()
        
        assert response == '401: Challenge verification failed!'