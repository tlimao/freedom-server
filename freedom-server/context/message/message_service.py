from aiohttp import web
from aiohttp.web_ws import WSMsgType
from freedomlib.message.message import Message
from freedomserver.context.message.message_repository import MessageRepository

class MessageService:

    def __init__(self, message_repository: MessageRepository):
        self._connected_clients = {}
        self._message_repository = message_repository

    async def handle_messages(self, ws: web.WebSocketResponse, account_id: str, device_id: str):
        async for msg in ws:
            if msg.type == WSMsgType.TEXT:
                message = Message.from_dict(msg.data)
                self._logger.info(f"Mensagem recebida de {account_id}: {message}")
                await self.process_message(account_id, device_id, message)
            elif msg.type == WSMsgType.ERROR:
                self._logger.error(f"Erro do cliente {account_id}: {ws.exception()}")
                break

    async def process_message(self, sender_account_id: str, sender_device_id: str, message: Message):
        recipient_id = message.recipient_id
        if recipient_id in self._connected_clients:
            await self.send_message(recipient_id, message)
        else:
            self._message_repository.store_message(recipient_id, message.to_dict())

    async def send_message(self, recipient_id: str, message: Message):
        for device_id, ws in self._connected_clients[recipient_id].items():
            await ws.send_str(message.to_json())