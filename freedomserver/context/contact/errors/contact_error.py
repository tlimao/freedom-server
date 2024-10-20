class ContactError(Exception):
    
    def __init__(self, message: str = None) -> None:
        super().__init__(message)
class ContactNotFoundError(ContactError):
    
    def __init__(self, message: str = "Contact Not Found") -> None:
        super().__init__(message)
