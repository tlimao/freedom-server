import logging
import argparse
from aiohttp.web import Application

from freedomserver.context.server.server_keys import ServerKeys
from freedomserver.server_routes import ServerRoutes
from freedomserver.server_config import ServerConfig


async def run(argv):
    parser = argparse.ArgumentParser(description="Freedom Server options")

    parser.add_argument('--config', '-c', type=str, help="Path to config file")
    parser.add_argument('--debug', '-d', type=str, help="True or False", default=False)
    
    options: argparse.Namespace = parser.parse_args(argv)
    
    server_keys: ServerKeys = ServerKeys()
    
    if (options.debug):
        logging.info("Debug mode enabled")
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    
    logging.info(f"Server Public Key:\n {server_keys.get_server_public_key_pem()}")
        
    config: ServerConfig = ServerConfig(server_keys, filename=options.config)
    
    app: Application = Application()
    
    ServerRoutes.setup_routes(app, config)
    
    return app