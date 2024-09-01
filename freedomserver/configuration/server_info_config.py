from dataclasses import dataclass

@dataclass
class ServerInfoConfig:
    name: str
    version: str
    environment: str
    
    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "version": self.version,
            "environment": self.environment
        }