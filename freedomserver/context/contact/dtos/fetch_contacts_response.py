from dataclasses import dataclass
from typing import List

from freedomlib.contact.contact import Contact
from freedomlib.utils.serializable import Serializable

@dataclass
class FetchContactsResponse(Serializable):
    
    contacts: List[Contact]
    
    def to_dict(self) -> List[dict]:
        return [contact.to_dict() for contact in self.contacts]

    