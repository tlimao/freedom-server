import base64
import json
import logging
from aiohttp import WSMsgType, web
from http import HTTPStatus
from freedomlib.message.message import Message
from freedomserver.context.message.message_service import MessageService
from freedomserver.context.auth.auth_service import AuthService
from freedomserver.context.server.server_keys import ServerKeys

class MessageController:

    def __init__(self, message_service: MessageService, auth_service: AuthService, server_keys: ServerKeys):
        self._message_service: MessageService = message_service
        self._auth_service: AuthService = auth_service
        self._connected_clients: dict[str, dict[str, web.WebSocketResponse]] = {}
        self._server_keys: ServerKeys = server_keys
        self._logger = logging.getLogger(__name__)

    async def message_handler(self, request: web.Request) -> web.WebSocketResponse:
        ws = web.WebSocketResponse()
        await ws.prepare(request)
        
        account_id, device_id = await self._authenticate(ws)
        if not account_id or not device_id:
            return ws
        
        
        self._logger.info(f"Nível de log atual: {self._logger.getEffectiveLevel()}")

        self._logger.debug(f"Cliente conectado: {account_id} - {device_id}")
        
        self._add_client(account_id, device_id, ws)
        
        messages: list[Message] = await self.recover_messages(account_id)

        if messages:
            for message in messages:
                await ws.send_json(message.to_dict())
                self._message_service.clear_account_messages(account_id, message.id)

        try:
            await self.handle_messages(ws, account_id, device_id)
        finally:
            self._remove_client(account_id, device_id)
            self._logger.debug(f"Cliente desconectado: {account_id} - {device_id}")
        
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
    
    async def handle_messages(self, ws: web.WebSocketResponse, account_id: str, device_id: str):
        async for msg in ws:
            if msg.type == WSMsgType.TEXT:
                message = Message.from_dict(json.loads(msg.data))
                self._logger.debug(f"Mensagem recebida de {account_id}: {message}")
                await self.process_message(account_id, device_id, message)
            elif msg.type == WSMsgType.ERROR:
                self._logger.error(f"Erro do cliente {account_id}: {ws.exception()}")
                break

    async def process_message(self, sender_account_id: str, sender_device_id: str, message: Message):
        recipient_id = message.recipient_id
        if recipient_id in self._connected_clients:
            await self.send_message(recipient_id, message)
        else:
            self._message_service.store_messages([message])

    async def recover_messages(self, account_id: str) -> list[Message]:
        return self._message_service.get_messages(account_id, 1)

    async def send_message(self, recipient_id: str, message: Message):
        for device_id, ws in self._connected_clients[recipient_id].items():
            await ws.send_str(json.dumps(message.to_dict()))
