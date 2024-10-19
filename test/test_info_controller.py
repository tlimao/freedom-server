from freedomserver.configuration.server_keys import ServerKeys
from freedomserver.context.info.info_routes import InfoRoutes
from freedomserver.configuration.server_info_config import ServerInfoConfig
from aiohttp import web
import pytest


@pytest.fixture
def server_info() -> ServerInfoConfig:
    return ServerInfoConfig(name="Freedom Server", version="1.0.0", environment="test")

@pytest.fixture
def server_keys() -> ServerKeys:
    return ServerKeys("dummy_public_key", "dummy_private_key")

async def test_get_info(aiohttp_client, server_info: ServerInfoConfig, server_keys: ServerKeys) -> None:
    app = web.Application()
    app.add_routes(InfoRoutes.create(server_info, server_keys))
    
    client = await aiohttp_client(app)
    
    async with client.get('/info') as resp:
        assert resp.status == 200
        response = await resp.json()
        assert response['name'] == server_info.name
        assert response['version'] == server_info.version
        assert response['environment'] == server_info.environment

async def test_get_server_pub_key(aiohttp_client, server_info: ServerInfoConfig, server_keys: ServerKeys) -> None:
    app = web.Application()
    app.add_routes(InfoRoutes.create(server_info, server_keys))
    
    client = await aiohttp_client(app)
    
    async with client.get('/pubkey') as resp:
        assert resp.status == 200
        response = await resp.json()
        assert response['serve_public_key'] == server_keys.public_key