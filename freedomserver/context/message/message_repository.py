from abc import ABC, abstractmethod
from typing import List
from freedomlib.message.message import Message

class MessageRepository(ABC):

    @abstractmethod
    def store_message(self, message: Message) -> None:
        pass

    @abstractmethod
    def get_messages(self, recipient_aci: str) -> List[Message]:
        pass

    @abstractmethod
    def delete_messages(self, recipient_aci: str) -> None:
        pass

    @abstractmethod
    def delete_message(self, recipient_aci: str, message_id: str) -> None:
        pass