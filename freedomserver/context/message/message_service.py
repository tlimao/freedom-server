import json
import logging
from aiohttp import web
from aiohttp.web_ws import WSMsgType
from freedomlib.message.message import Message
from freedomserver.context.connections.ws_connection_manager import ConnectionId
from freedomserver.context.message.message_repository import MessageRepository

class MessageService:

    def __init__(self, message_repository: MessageRepository):
        self._connected_clients = {}
        self._message_repository = message_repository

    async def handle_messages(self, ws: web.WebSocketResponse):
        async for msg in ws:
            if msg.type == WSMsgType.TEXT:
                message = Message.from_dict(json.loads(msg.data))
                logging.info(f"Mensagem recebida de {message.sender_aci}: {message}")
                await self.process_message(message)
            elif msg.type == WSMsgType.ERROR:
                logging.error(f"Erro do cliente {message.sender_aci}: {ws.exception()}")
                break

    async def process_message(self, message: Message):
        recipient_aci: str = message.recipient_aci
        if recipient_aci in self._connected_clients:
            await self.send_message(message)
        else:
            self._message_repository.store_message(message)

    async def send_message(self, message: Message):
        for device_id, ws in self._connected_clients[message.recipient_aci].items():
            await ws.send_str(message.to_dict())