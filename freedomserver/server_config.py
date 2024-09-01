import logging

from yaml import safe_load

from freedomserver.configuration.redis_config import RedisConfig

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
        except Exception as e:
            logging.error(f"Can't load config from {filename}: {e}")

    def _load_from_env(self) -> None:
        ...