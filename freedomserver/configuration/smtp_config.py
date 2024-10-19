from dataclasses import dataclass

@dataclass
class SmtpConfig:

    host: str
    port: str
    user: str
    password: str
    tls: bool = True