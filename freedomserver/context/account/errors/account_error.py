class AccountError(Exception):
    
    def __init__(self, message: str = None) -> None:
        super().__init__(message)
        
    @classmethod
    def _format_message(cls, base_message: str, additional_message: str = None) -> str:
        return f"{base_message} : {additional_message}" if additional_message else base_message
class AccountNotFoundError(AccountError):
    
    def __init__(self, message: str = "Account Not Found") -> None:
        super().__init__(message)
class AccountNotCreatedError(AccountError):
    
    def __init__(self, message: str = "Account Not Created") -> None:
        super().__init__(message)
class AccountRegistrationError(AccountError):

    def __init__(self, message: str = "Account Registration Failed") -> None:
        super().__init__(message)