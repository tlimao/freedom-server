import json
import logging
import argparse
from aiohttp.web import Application

from freedomserver.commands.server_keys import generate_server_keys
from freedomserver.context.utils.banner import Banner
from freedomserver.server_routes import ServerRoutes
from freedomserver.server_config import ServerConfig

async def run(argv):
    parser = argparse.ArgumentParser(description="Freedom Server options")

    parser.add_argument('--config', '-c', type=str, help="Path to config file")
    parser.add_argument('--debug', '-d', type=str, help="True or False", default=False)
    parser.add_argument('--command', type=str, help="Commands:\ngenerateServerKeys", default=None)
    
    options: argparse.Namespace = parser.parse_args(argv)
    
    if (options.command == "generateServerKeys"):
        keys: dict = generate_server_keys()
        print(json.dumps(keys, indent=4))
        return
    
    if (options.debug):
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    
    config: ServerConfig = ServerConfig(filename=options.config)
    
    app: Application = Application()
    
    ServerRoutes.setup_routes(app, config)
    
    Banner.show(config.server_info)
    
    return app