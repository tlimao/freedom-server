deactivate
source .env/bin/activate

python -m aiohttp.web -H 0.0.0.0 -P 8080 freedomserver.server_run:run -c config/server.local.yml