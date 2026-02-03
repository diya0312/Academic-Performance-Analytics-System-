# tests/unit/test_crypto_extra_2.py
import os
from unittest.mock import patch
from backend.crypto import get_fernet, get_hmac_key, encrypt_value, decrypt_value


def test_env_var_fernet_key_valid(monkeypatch):
    # valid base64 32-byte Fernet key
    key = b"Z" * 32
    import base64
    good_key = base64.urlsafe_b64encode(key).decode()

    monkeypatch.setenv("APAS_FERNET_KEY", good_key)
    f = get_fernet()
    token = f.encrypt(b"hello")
    assert f.decrypt(token) == b"hello"


def test_env_var_hmac_key(monkeypatch):
    monkeypatch.setenv("APAS_HMAC_KEY", "abc123")
    hk = get_hmac_key()
    assert hk == b"abc123"


def test_encrypt_decrypt_edge_cases():
    t = encrypt_value("x")
    assert decrypt_value(t) == "x"

    # ensure invalid fernet token returns None
    assert decrypt_value("invalid_token") is None
