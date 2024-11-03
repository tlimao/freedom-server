import logging

from freedomserver.configuration.server_info_config import ServerInfoConfig


class Banner:
    
    BANNER_FILE: str = "./freedomserver/resources/banner/server.txt"
    
    @classmethod
    def show(cls, server_info: ServerInfoConfig) -> None:
        with open(cls.BANNER_FILE, 'r') as f:
            banner: str = f.read()
            banner = banner.replace("{version}", server_info.version)
            banner = banner.replace("{environment}", server_info.environment)
            logging.info(banner)