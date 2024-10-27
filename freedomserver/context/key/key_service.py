import json

from freedomserver.context.utils.generate_ids import generate_uuid7_str

from freedomlib.key.key import Key
from freedomlib.key.key_repository import KeyRepository

from freedomserver.context.key.dtos.key_data import KeyData
from freedomserver.context.key.errors.key_error import KeyNotDeletedError, KeyNotFoundError, KeyNotStoredError

class KeyService:
    
    def __init__(self, key_repository: KeyRepository) -> None:
        self._key_repository: KeyRepository = key_repository

    def store_key(self, key_data: KeyData) -> None:
        try:
            key: Key = Key(
                id=generate_uuid7_str(),
                aci=key_data.aci,
                ed25519_pub_key=key_data.ed25519_pub_key
            )

            self._key_repository.save(key)
        except Exception as e:
            raise KeyNotStoredError(message=e)

    def get_key(self, aci: str) -> Key:
        try:
            key: Key = self._key_repository.get_key_by_aci(aci)
            
            if not key:
                raise KeyNotFoundError()
            
            return key
            
        except Exception as e:
            raise KeyNotFoundError(message=e)

    def delete_key(self, aci: str) -> None:
        try:
            self._key_repository.delete(aci)
        except Exception as e:
            raise KeyNotDeletedError(message=e)