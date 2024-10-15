import logging

from yaml import safe_load

from freedomserver.configuration.redis_config import RedisConfig
from freedomserver.configuration.server_info_config import ServerInfoConfig
from freedomserver.configuration.server_keys import ServerKeys

logger = logging.getLogger(__name__)

class ServerConfig:
    
    def __init__(self, filename: str = None) -> None:
        if (filename):
            self._load_from_file(filename)
        else:
            self._load_from_env()

    def _load_from_file(self, filename: str) -> None:
        try:
            with open(filename) as f:
                config_dict: dict = safe_load(f.read())
                
                self._redis_config: RedisConfig = RedisConfig(**config_dict.get("redis"))
                self._server_info: ServerInfoConfig = ServerInfoConfig(**config_dict.get("server_info"))
                self._server_keys: ServerKeys = ServerKeys(**config_dict.get("server_keys"))
        except Exception as e:
            logging.error(f"Can't load config from {filename}: {e}")

    @property
    def redis_config(self) -> RedisConfig:
        return self._redis_config
    
    @property
    def server_info(self) -> ServerInfoConfig:
        return self._server_info

    @property
    def server_keys(self) -> ServerKeys:
        return self._server_keys

    def _load_from_env(self) -> None:
        ...