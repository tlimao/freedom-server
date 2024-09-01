from freedomserver.context.info.info_routes import InfoRoutes
from freedomserver.configuration.server_info_config import ServerInfoConfig
from aiohttp import web
import pytest


@pytest.fixture
def server_info() -> ServerInfoConfig:
    return ServerInfoConfig(name="Freedom Server", version="1.0.0", environment="test")

async def test_get_info(aiohttp_client, server_info: ServerInfoConfig):
    app = web.Application()
    app.add_routes(InfoRoutes.create(server_info))
    
    client = await aiohttp_client(app)
    
    async with client.get('/info') as resp:
        assert resp.status == 200
        response = await resp.json()
        assert response['name'] == 'Freedom Server'
        assert response['version'] == '1.0.0'
        assert response['environment'] == 'test'