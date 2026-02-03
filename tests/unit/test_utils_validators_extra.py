from src.backend.utils.validators import is_valid_string, is_valid_number

def test_is_valid_string_good():
    assert is_valid_string("hello")

def test_is_valid_string_strip():
    assert not is_valid_string("   ")

def test_is_valid_string_not_str():
    assert not is_valid_string(100)

def test_is_valid_number_valid():
    assert is_valid_number("3.14")
    assert is_valid_number(15)

def test_is_valid_number_invalid():
    assert not is_valid_number("abc")
