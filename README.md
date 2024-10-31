# Freedom Server

## Requirements

```
python 3.9+

* Tested and develop in python 3.13
```

## Install Dependencies

```
python -m pip install -r requirements.txt
```

## Run local

```
python -m aiohttp.web -H 0.0.0.0 -P 8080 freedomserver.server_run:run -c config/server.local.yml
```