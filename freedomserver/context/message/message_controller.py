import base64
import json
import logging
from aiohttp import WSMsgType, web
from http import HTTPStatus
from freedomserver.context.connections.ws_connection_manager import WsConnectionManager
from freedomserver.context.message.message_service import MessageService
from freedomserver.context.auth.auth_service import AuthService
routes = web.RouteTableDef()

class MessageController:

    def __init__(self, message_service: MessageService):
        self._message_service: MessageService = message_service
        self._connection_manager: WsConnectionManager = WsConnectionManager()
        self._logger = logging.getLogger(__name__)

    async def message_handler(self, request: web.Request) -> web.WebSocketResponse:
        ws = web.WebSocketResponse()
        await ws.prepare(request)
        
        account_id, device_id = await self._authenticate(ws)
        if not account_id or not device_id:
            return ws

        self._logger.info(f"Client connected: {account_id} - {device_id}")
        
        self._connection_manager.add_client(account_id, device_id, ws)
        
        try:
            await self._message_service.handle_messages(ws, account_id, device_id)
        finally:
            self._connection_manager.remove_client(account_id, device_id)
            self._logger.info(f"Client disconnected: {account_id} - {device_id}")
        
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
