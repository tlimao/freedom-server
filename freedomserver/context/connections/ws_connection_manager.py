from abc import ABC
from dataclasses import dataclass


@dataclass
class WsConnectionManager(ABC):
    
    def __init__(self) -> None:
        self._connections: dict = {}

    def get_ws(self, account_id: str, device_id: str) -> None: