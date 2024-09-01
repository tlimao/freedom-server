from abc import ABC, abstractmethod

class AuthRepository(ABC):

    @abstractmethod
    def register_device(self, public_key: str, device_id: str) -> str:
        pass

    @abstractmethod
    def store_challenge(self, account_id: str, device_id: str, challenge: str) -> None:
        pass

    @abstractmethod
    def get_challenge(self, account_id: str, device_id: str) -> str:
        pass
