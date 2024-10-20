
from aiohttp import web

class WsConnectionManager:
    
    def __init__(self) -> None:
        self._connected_clients: dict[str, dict[str, web.WebSocketResponse]] = {}

    def add_client(self, account_id: str, device_id: str, ws: web.WebSocketResponse):
        self._connected_clients.setdefault(account_id, {})[device_id] = ws

    def remove_client(self, account_id: str, device_id: str):
        if account_id in self._connected_clients:
            self._connected_clients[account_id].pop(device_id, None)
            if not self._connected_clients[account_id]:
                del self._connected_clients[account_id]