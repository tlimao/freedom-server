from dataclasses import dataclass, field


@dataclass(frozen=True)
class RedisConfig:
    
    host: str
    port: int = field(default=6379)
    password: str