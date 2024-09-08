from typing import List

from freedomlib.message.message import Message
from freedomlib.message.message_repository import MessageRepository

class MessageService:

    MESSAGE_DIRECTORY: str = "chat:message"
    EXPIRATION_TIME: int = 30 * 24 * 60 * 60

    def __init__(self, message_repository: MessageRepository) -> None:
        self._message_repository: MessageRepository = message_repository

    def store_messages(self, messages: List[Message]) -> None:
        self._message_repository.save_with_expiration(messages, self.EXPIRATION_TIME)

    def get_messages(self, account_id: str, device_id: str) -> List[Message]:
        return self._message_repository.get(account_id)

    def clear_messages(self, account_id: str, message_id: str) -> None:
        self._message_repository.delete(account_id, message_id)

    def clear_account_messages(self, account_id: str, message_id: str) -> None:
        self._message_repository.delete_for_me(account_id, message_id)

    def update_message(self, message: Message) -> None:
        self._message_repository.update(message)