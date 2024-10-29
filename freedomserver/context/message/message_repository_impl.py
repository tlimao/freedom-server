import json
from redis import Redis

from freedomlib.message.message import Message

from freedomserver.context.message.message_repository import MessageRepository

class MessageRepositoryImpl(MessageRepository):
    
    MESSAGE_QUEUE: str = "chat:message_queue"
    
    MESSAGE_EXPIRATION: int = 60 * 60 * 24 * 7  # 7 dias

    def __init__(self, redis_connection: Redis):
        self._redis_connection = redis_connection

    def store_message(self, recipient_id: str, message: Message) -> None:
        message_data = {
            "recipient_id": recipient_id,
            "message": message.to_json()
        }
        self._redis_connection.lpush(self.MESSAGE_QUEUE, json.dumps(message_data))
        self._redis_connection.expire(self.MESSAGE_QUEUE, self.MESSAGE_EXPIRATION)

    def get_messages(self, recipient_id: str, count: int = 10) -> list[Message]:
        messages = []
        for _ in range(count):
            message_data = self._redis_connection.rpop(self.MESSAGE_QUEUE)
            if message_data:
                data = json.loads(message_data)
                if data["recipient_id"] == recipient_id:
                    messages.append(Message.from_json(data["message"]))
                else:
                    # Se a mensagem não for para o destinatário atual, coloque-a de volta na fila
                    self._redis_connection.rpush(self.MESSAGE_QUEUE, message_data)
            else:
                break
        return messages

    def delete_messages(self, recipient_id: str) -> None:
        # Não é necessário implementar esta função para uma fila
        pass

    def delete_message(self, recipient_id: str, message_id: str) -> None:
        return super().delete_message(recipient_id, message_id)