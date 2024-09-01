import logging
import argparse
from aiohttp.web import Application

from freedomserver.server_routes import ServerRoutes

async def run(argv):
    parser = argparse.ArgumentParser(description="Freedom Server options")

    parser.add_argument('--config', '-c', type=str, help="Path to config file")
    parser.add_argument('--debug', '-d', type=str, help="True or False", default=False)
    
    options: argparse.Namespace = parser.parse_args(argv)
    
    if (options.debug):
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    
    app: Application = Application()
    
    ServerRoutes.setup_routes(app)
    
    return app