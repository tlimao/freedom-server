import base64
import logging
from aiohttp import WSMsgType, web
from http import HTTPStatus
from freedomlib.message.message_manager import MessageManager

routes = web.RouteTableDef()

class MessageController:

    def __init__(self, message_manager: MessageManager):
        self._message_manager: MessageManager = message_manager
        self._connected_clients: dict[str, dict[str, web.WebSocketResponse]] = {}
        self._logger = logging.getLogger(__name__)

    async def message_handler(self, request: web.Request) -> web.WebSocketResponse:
        ws = web.WebSocketResponse()
        await ws.prepare(request)
        
        account_id, device_id = await self._authenticate(request)
        if not account_id:
            return web.HTTPUnauthorized(reason="Autenticação inválida")

        self._logger.info(f"Cliente conectado: {account_id} - {device_id}")
        
        self._add_client(account_id, device_id, ws)
        
        try:
            await self._handle_messages(ws, account_id, device_id)
        finally:
            self._remove_client(account_id, device_id)
            self._logger.info(f"Cliente desconectado: {account_id} - {device_id}")
        
        return ws
    async def _authenticate(self, request: web.Request) -> tuple[str | None, str | None]:
        auth_header = request.headers.get('Authorization')
        print(auth_header)
        if not auth_header or not auth_header.startswith('Basic '):
            print("auth_header is not valid 1")
            return None, None

        try:
            auth_value = auth_header.split(' ')[1]
            parts = auth_value.split('.')
            return parts[0], parts[1]
        except (ValueError, IndexError):
            print("auth_header is not valid 2")
            return None, None

    def _add_client(self, account_id: str, device_id: str, ws: web.WebSocketResponse):
        self._connected_clients.setdefault(account_id, {})[device_id] = ws

    def _remove_client(self, account_id: str, device_id: str):
        if account_id in self._connected_clients:
            self._connected_clients[account_id].pop(device_id, None)
            if not self._connected_clients[account_id]:
                del self._connected_clients[account_id]

    async def _handle_messages(self, ws: web.WebSocketResponse, account_id: str, device_id: str):
        async for msg in ws:
            if msg.type == WSMsgType.TEXT:
                self._logger.info(f"Mensagem recebida de {account_id}: {msg.data}")
                await self._broadcast_message(account_id, device_id, msg.data)
            elif msg.type == WSMsgType.ERROR:
                self._logger.error(f"Erro do cliente {account_id}: {ws.exception()}")
                break

    async def _broadcast_message(self, sender_account_id: str, sender_device_id: str, message: str):
        for account_id, devices in self._connected_clients.items():
            for device_id, ws in devices.items():
                if account_id != sender_account_id or device_id != sender_device_id:
                    await ws.send_str(f"Cliente {sender_account_id} diz: {message}")
