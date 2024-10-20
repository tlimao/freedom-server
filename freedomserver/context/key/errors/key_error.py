class KeyError(Exception):
    
    def __init__(self, message: str = None) -> None:
        super().__init__(message)

class KeyNotFoundError(KeyError):
    
    def __init__(self, message: str = "Key Not Found") -> None:
        super().__init__(message)

class KeyNotStoredError(KeyError):
    
    def __init__(self, message: str = "Key Not Stored") -> None:
        super().__init__(message)

class KeyNotDeletedError(KeyError):
    
    def __init__(self, message: str = "Key Not Deleted") -> None:
        super().__init__(message)