from abc import ABC
from freedomlib.account.account import Account


class AccountRepository(ABC):

    def save(self, account: Account) -> Account:
        raise NotImplementedError()
    
    def get_by_aci(self, aci: str) -> Account | None:
        raise NotImplementedError()

    def get_by_email(self, email: str) -> Account | None:
        raise NotImplementedError()

    def get_by_phonenumber(self, phonenumber: str) -> Account | None:
        raise NotImplementedError()

    def update(self, account: Account) -> Account:
        raise NotImplementedError()

    def delete(self, aci: str) -> None:
        raise NotImplementedError()
    