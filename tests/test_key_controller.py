import pytest
from fakeredis import FakeRedis
from aiohttp import web

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PublicKey

from freedomlib.key.key_box import KeyBox
from freedomserver.context.key.key_routes import KeyRoutes
from freedomserver.context.key.repository.key_repository import KeyRepository
from freedomserver.context.key.repository.key_repository_impl import KeyRepositoryImpl
from tests.commons import ED25519_PUBLIC_KEY, RICKY_SANCHEZ_ACI, X25519_PUBLIC_KEY

@pytest.fixture
def fake_redis() -> FakeRedis:
    # Cria uma conexão fake do Redis usando fakeredis
    return FakeRedis()

@pytest.fixture
def key_repository(fake_redis: FakeRedis) -> KeyRepository:
    key_repository: KeyRepository = KeyRepositoryImpl(fake_redis)
    
    key_repository.save(KeyBox(
        id="dummy-id",
        aci=RICKY_SANCHEZ_ACI,
        ed25519_public_key=ED25519_PUBLIC_KEY,
        x25519_public_key=X25519_PUBLIC_KEY
    ))
    
    return key_repository

async def test_get_account_key(
    aiohttp_client,
    key_repository: KeyRepository):
    
    app = web.Application()
    app.add_routes(KeyRoutes.create(key_repository=key_repository))
    
    client = await aiohttp_client(app)
        
    async with client.get(f'/key/{RICKY_SANCHEZ_ACI}') as resp:
        assert resp.status == 200
        response = await resp.json()
        key_box: KeyBox = KeyBox(**response)
        
        assert key_box.aci == RICKY_SANCHEZ_ACI 
        assert key_box.ed25519_public_key == ED25519_PUBLIC_KEY
        assert key_box.x25519_public_key == X25519_PUBLIC_KEY
        assert isinstance(key_box.load_signing_key(), Ed25519PublicKey)
        assert isinstance(key_box.load_exchange_key(), X25519PublicKey)

async def test_get_invalid_account_key(
    aiohttp_client,
    key_repository: KeyRepository):
    
    app = web.Application()
    app.add_routes(KeyRoutes.create(key_repository=key_repository))
    
    client = await aiohttp_client(app)
        
    async with client.get('/key/invalid_account_aci') as resp:
        assert resp.status == 404
        response = await resp.text()
        
        assert response == "404: Key Not Found"