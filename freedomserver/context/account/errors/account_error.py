class AccountError(Exception):
    
    def __init__(self, message: str = None) -> None:
        super().__init__(message)
class AccountNotFoundError(AccountError):
    
    def __init__(self, message: str = "Account Not Found") -> None:
        super().__init__(message)
class AccountNotCreatedError(AccountError):
    
    def __init__(self, message: str = "Account Not Created") -> None:
        super().__init__(message)
class AccountRegistrationError(AccountError):

    def __init__(self, message: str = "Account Registration Failed") -> None:
        super().__init__(message)
        
class AccountVerificationError(AccountError):

    def __init__(self, message: str = "Account Verification Failed") -> None:
        super().__init__(message)
        
class AccountUpdateError(AccountError):
    
    def __init__(self, message: str = "Account not Updated") -> None:
        super().__init__(message)