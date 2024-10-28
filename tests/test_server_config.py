from yaml import safe_load
from freedomserver.server_config import ServerConfig


CONFIG_FILENAME: str = "./tests/resources/test_config.yml"

def test_load_config_file() -> None:
    with open(CONFIG_FILENAME) as f:
        server_config_check: dict = safe_load(f.read())
    
    
    server_config: ServerConfig = ServerConfig(CONFIG_FILENAME)
    
    assert server_config.redis_config.host == server_config_check["redis"]["host"]
    assert server_config.redis_config.port == server_config_check["redis"]["port"]
    assert server_config.redis_config.password == server_config_check["redis"]["password"]
    
    assert server_config.server_info.name == server_config_check["server_info"]["name"]
    assert server_config.server_info.version == server_config_check["server_info"]["version"]
    assert server_config.server_info.environment == server_config_check["server_info"]["environment"]
    
    assert server_config.smtp_config.host == server_config_check["smtp"]["host"]
    assert server_config.smtp_config.port == server_config_check["smtp"]["port"]
    assert server_config.smtp_config.user == server_config_check["smtp"]["user"]
    assert server_config.smtp_config.password == server_config_check["smtp"]["password"]
    assert server_config.smtp_config.tls == server_config_check["smtp"]["tls"]
    
    assert server_config.server_keys.private_key == server_config_check["server_keys"]["private_key"]
    assert server_config.server_keys.public_key == server_config_check["server_keys"]["public_key"]