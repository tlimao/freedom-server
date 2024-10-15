class AccountError(Exception):
    
    def __init__(self, message: str = None) -> None:
        super().__init__(message)
        
class AccountNotFoundError(AccountError):
    
    def __init__(self, message: str = "Account Not Found!") -> None:
        super().__init__(message)

class AccountNotCreatedError(AccountError):
    
    def __init__(self, message: str = "Account Not Created!") -> None:
        super().__init__(message)