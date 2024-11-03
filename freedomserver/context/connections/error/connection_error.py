class ConnectionError(Exception):
    
    def __init__(self, message: str) -> None:
        super().__init__(message)

class AuthFailed(ConnectionError):
    
    def __init__(self, message: str) -> None:
        super().__init__(message)