
import json
from dataclasses import dataclass
from aiohttp import web_app, WSMsgType, web

from freedomserver.context.auth.auth_service import AuthService
from freedomserver.context.connections.error.connection_error import AuthFailed


WS_AUTHENTICATE: str = "AUTHENTICATE"

@dataclass
class ConnectionId:
    
    aci: str
    device_id: str
    
    def __str__(self) -> str:
        return f"{self.aci}:{self.device_id}"

class WsConnectionManager:
    
    def __init__(self, auth_service: AuthService) -> None:
        self._auth_service: AuthService = auth_service
        self._connected_clients: dict[str, dict[str, web.WebSocketResponse]] = {}

    def add_client(self, connection_id: ConnectionId, ws: web.WebSocketResponse) -> None:
        self._connected_clients.setdefault(
            connection_id.aci, {})[connection_id.device_id] = ws

    def remove_client(self, connection_id: ConnectionId) -> None:
        if connection_id.aci in self._connected_clients:
            self._connected_clients[connection_id.aci].pop(connection_id.device_id, None)
            if not self._connected_clients[connection_id.aci]:
                del self._connected_clients[connection_id.aci]

    async def authenticate(self, ws: web.WebSocketResponse) -> ConnectionId:
        await ws.send_str(WS_AUTHENTICATE)
        
        try:
            msg = await ws.receive_str()
            auth_data: dict = json.loads(msg)
            
            aci = auth_data.get('aci')
            device_id = auth_data.get('device_id')
            token = auth_data.get('token')
            
            if not aci or not device_id or not token:
                raise AuthFailed("Invalid Auth data")
            
            if not self._auth_service.verify_token(aci, device_id, token):
                raise AuthFailed("Auth failed")
            
            return ConnectionId(aci, device_id)

        except json.JSONDecodeError:
            await ws.close(code=WSMsgType.CLOSE, message="Invalid Auth format")
            raise AuthFailed("Invalid Auth format")

        except AuthFailed as e:
            await ws.close(code=WSMsgType.CLOSE, message=str(e))
            raise e