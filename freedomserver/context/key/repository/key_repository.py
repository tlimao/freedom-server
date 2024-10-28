from abc import ABC

from freedomlib.key.key_box import KeyBox

class KeyRepository(ABC):

    def save(self, key_box: KeyBox) -> KeyBox:
        raise NotImplementedError()

    def get_key_by_aci(self, aci: str) -> KeyBox | None:
        raise NotImplementedError()

    def get(self, key_box_id: str) -> KeyBox:
        raise NotImplementedError()

    def delete(self, key_box_id: str) -> None:
        raise NotImplementedError()

    def update(self, key_box: KeyBox) -> KeyBox:
        raise NotImplementedError()

