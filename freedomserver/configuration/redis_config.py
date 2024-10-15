from dataclasses import dataclass, field


@dataclass(frozen=True)
class RedisConfig:
    
    host: str
    port: int = field(default=6379)
    password: str = field(default="")
    
    @property
    def host(self) -> str:
        return self.host

    @property
    def port(self) -> int:
        return self.port

    @property
    def password(self) -> str:
        return self.password

    