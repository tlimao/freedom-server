from abc import ABC, abstractmethod

from freedomlib.key.key import Key

class AuthRepository(ABC):

    @abstractmethod
    def store_challenge(self, aci: str, device_id: str, challenge: str) -> None:
        raise NotImplementedError()

    @abstractmethod
    def get_challenge(self, aci: str, device_id: str) -> str:
        raise NotImplementedError()

    @abstractmethod
    def delete_challenge(self, aci: str, device_id: str) -> None:
        raise NotImplementedError()

    @abstractmethod
    def store_token(self, aci: str, device_id: str, token: str) -> None:
        raise NotImplementedError()

    @abstractmethod
    def get_token(self, aci: str, device_id: str) -> str:
        raise NotImplementedError()

    @abstractmethod
    def delete_token(self, aci: str, device_id: str) -> None:
        raise NotImplementedError()

    @abstractmethod
    def store_ed25519_key(self, ed25519_key: str) -> None:
        raise NotImplementedError()

    @abstractmethod
    def get_ed25519_key(self, aci: str) -> Key:
        raise NotImplementedError()
        
