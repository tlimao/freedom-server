from abc import ABC, abstractmethod

class AuthRepository(ABC):

    @abstractmethod
    def store_challenge(self, account_id: str, device_id: str, challenge: str) -> None:
        pass

    @abstractmethod
    def get_challenge(self, account_id: str, device_id: str) -> str:
        pass

    @abstractmethod
    def delete_challenge(self, account_id: str, device_id: str) -> None:
        pass

    @abstractmethod
    def store_token(self, account_id: str, device_id: str, token: str) -> None:
        pass

    @abstractmethod
    def get_token(self, account_id: str, device_id: str) -> str:
        pass

    @abstractmethod
    def delete_token(self, account_id: str, device_id: str) -> None:
        pass
