import uuid6

from freedomserver.context.utils.generate_ids import generate_number_id_str, generate_uuid7_str, generate_verification_code


def test_generate_uuid7_str() -> None:
    uuid7: str = generate_uuid7_str()
    
    assert isinstance(uuid7, str)

def test_is_uuid7_valid() -> None:
    uuid7: str = generate_uuid7_str()
    
    assert isinstance(uuid6.UUID(hex=uuid7), uuid6.UUID)

def text_generate_number_id_str() -> None:
    number_id: str = generate_number_id_str()
    
    assert len(number_id) == 6
    assert isinstance(number_id, str)

def test_generate_verification_token() -> None:
    verification_token: str = generate_verification_code()
    
    assert len(verification_token) == 6
    assert isinstance(verification_token, str)