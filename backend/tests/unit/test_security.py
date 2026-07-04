"""Tests de seguridad"""

import pytest

from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    decode_token,
)


def test_hash_password():
    """Test hashing de contraseña"""
    password = "test_password_123"
    hashed = hash_password(password)

    assert hashed != password
    assert verify_password(password, hashed)
    assert not verify_password("wrong_password", hashed)


def test_create_and_decode_token():
    """Test creación y decodificación de tokens"""
    data = {"sub": "user@example.com", "user_id": 1}
    token = create_access_token(data)

    assert token is not None
    decoded = decode_token(token)
    assert decoded is not None
    assert decoded["sub"] == "user@example.com"
    assert decoded["user_id"] == 1


def test_invalid_token():
    """Test decodificación de token inválido"""
    result = decode_token("invalid.token.here")
    assert result is None
