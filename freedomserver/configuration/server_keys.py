from dataclasses import dataclass


@dataclass
class ServerKeys:
    
    public_key: str
    private_key: str