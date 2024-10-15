import base64
import json
import logging
from aiohttp import WSMsgType, web
from http import HTTPStatus
from freedomserver.context.message.message_service import MessageService
from freedomlib.message.message_manager import MessageManager
from freedomserver.context.auth.auth_service import AuthService
routes = web.RouteTableDef()

class MessageController:

    def __init__(self, message_manager: MessageManager, auth_service: AuthService):
        self._message_manager: MessageManager = message_manager
        self._auth_service: AuthService = auth_service
        self._connected_clients: dict[str, dict[str, web.WebSocketResponse]] = {}
        self._logger = logging.getLogger(__name__)
        self._message_service = MessageService()

    async def message_handler(self, request: web.Request) -> web.WebSocketResponse:
        ws = web.WebSocketResponse()
        await ws.prepare(request)
        
        account_id, device_id = await self._authenticate(ws)
        if not account_id or not device_id:
            return ws

        self._logger.info(f"Cliente conectado: {account_id} - {device_id}")
        
        self._add_client(account_id, device_id, ws)
        
        try:
            await self._message_service.handle_messages(ws, account_id, device_id)
        finally:
            self._remove_client(account_id, device_id)
            self._logger.info(f"Cliente desconectado: {account_id} - {device_id}")
        
        return ws
    
    async def _authenticate(self, ws: web.WebSocketResponse):
        await ws.send_str("AUTHENTICATE")
        
        try:
            msg = await ws.receive_str()
            auth_data = json.loads(msg)
            
            account_id = auth_data.get('account_id')
            device_id = auth_data.get('device_id')
            token = auth_data.get('token')
            
            if not account_id or not device_id or not token:
                await ws.close(code=WSMsgType.CLOSE, message="Dados de autenticação inválidos")
                return None, None
            
            if not self._validate_token(account_id, device_id, token):
                await ws.close(code=WSMsgType.CLOSE, message="Autenticação falhou")
                return None, None
            
            return account_id, device_id
        except json.JSONDecodeError:
            self._logger.error("Erro ao decodificar JSON de autenticação")
            await ws.close(code=WSMsgType.CLOSE, message="Formato de autenticação inválido")
            return None, None
        except Exception as e:
            self._logger.error(f"Erro durante a autenticação: {str(e)}")
            await ws.close(code=WSMsgType.CLOSE, message="Erro de autenticação")
            return None, None

    def _validate_token(self, account_id: str, device_id: str, token: str) -> bool:
        return self._auth_service.verify_token(account_id, device_id, token)

    def _add_client(self, account_id: str, device_id: str, ws: web.WebSocketResponse):
        self._connected_clients.setdefault(account_id, {})[device_id] = ws

    def _remove_client(self, account_id: str, device_id: str):
        if account_id in self._connected_clients:
            self._connected_clients[account_id].pop(device_id, None)
            if not self._connected_clients[account_id]:
                del self._connected_clients[account_id]
