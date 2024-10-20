import base64
import uuid6
import secrets


def generate_uuid7_str() -> str:
    return str(uuid6.uuid7())

def generate_number_id_str(size: int = 6) -> str:
    return "111111"
    # return str(secrets.randbelow(9*(10**(size-1))) + 10**(size-1))

def generate_verification_code(size: int = 6) -> str:
    return "111111"
    # return str(secrets.randbelow(9*(10**(size-1))) + 10**(size-1))