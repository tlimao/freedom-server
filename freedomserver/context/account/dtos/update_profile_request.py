from dataclasses import dataclass

from freedomserver.context.account.dtos.account_profile import AccountProfile


@dataclass
class UpdateProfileRequest:

    account_profile: AccountProfile

    @classmethod
    def from_dict(cls, data: dict) -> 'UpdateProfileRequest':
        return UpdateProfileRequest(
            account_profile=AccountProfile(**data.get('account_profile'))
        )