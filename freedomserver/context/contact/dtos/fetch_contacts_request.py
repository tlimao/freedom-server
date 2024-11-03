from dataclasses import dataclass
from typing import List


@dataclass
class FetchContactsRequest:
    
    phonenumbers: List[str]
    acis: List[str]

    @classmethod
    def from_dict(cls, data: dict) -> 'FetchContactsRequest':
        return FetchContactsRequest(**data)