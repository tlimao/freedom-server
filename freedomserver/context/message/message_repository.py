from abc import ABC, abstractmethod
from freedomlib.message.message import Message

class MessageRepository(ABC):

    @abstractmethod
    def store_message(self, recipient_id: str, message: Message) -> None:
        pass

    @abstractmethod
    def get_messages(self, recipient_id: str) -> list[Message]:
        pass

    @abstractmethod
    def delete_messages(self, recipient_id: str) -> None:
        pass

    @abstractmethod
    def delete_message(self, recipient_id: str, message_id: str) -> None:
        pass