from dataclasses import dataclass


@dataclass
class ServerKeys:
    
    public_key: str
    private_key: str
    
    @property
    def public_key(self) -> str:
        return self.public_key
    
    @property
    def private_key(self) -> str:
        return self.private_key