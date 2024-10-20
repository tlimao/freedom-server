from dataclasses import dataclass

from freedomlib.utils.serializable import Serializable

from freedomserver.context.account.dtos.account_profile import AccountProfile

@dataclass
class UpdateProfileResponse(Serializable):

    account_profile: AccountProfile

    def to_dict(self) -> dict:
        return self.account_profile.to_dict()