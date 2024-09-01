import logging

from yaml import safe_load

from freedomserver.configuration.redis_config import RedisConfig
from freedomserver.configuration.server_info_config import ServerInfoConfig

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
        except Exception as e:
            logging.error(f"Can't load config from {filename}: {e}")
            
    def get_redis_config(self) -> RedisConfig:
        return self._redis_config
    
    def get_server_info(self) -> ServerInfoConfig:
        return self._server_info

    def _load_from_env(self) -> None:
        ...