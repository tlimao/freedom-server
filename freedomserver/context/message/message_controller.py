import logging

from aiohttp import web
from freedomserver.context.connections.error.connection_error import AuthFailed
from freedomserver.context.connections.ws_connection_manager import ConnectionId, WsConnectionManager
from freedomserver.context.message.message_service import MessageService
from freedomserver.context.auth.auth_service import AuthService

class MessageController:

    def __init__(self, message_service: MessageService, auth_service: AuthService):
        self._message_service: MessageService = message_service
        self._auth_service: AuthService = auth_service
        self._connection_manager: WsConnectionManager = WsConnectionManager(self._auth_service)
        self._logger = logging.getLogger(__name__)

    async def message_handler(self, request: web.Request) -> web.WebSocketResponse:
        ws = web.WebSocketResponse()
        await ws.prepare(request)
        
        try:
            connection_id: ConnectionId = await self._connection_manager.authenticate(ws)
            
            self._logger.info(f"Client connected: {str(connection_id)}")
            
            self._connection_manager.add_client(connection_id, ws)
            
            try:
                await self._message_service.handle_messages(ws)
            finally:
                self._connection_manager.remove_client(connection_id)
                self._logger.info(f"Client disconnected: {str(connection_id)}")
            
        except AuthFailed as e:
            logging.error(str(e))
        
        return ws