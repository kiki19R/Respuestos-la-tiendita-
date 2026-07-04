"""Módulo de seguridad - JWT, Bcrypt, autenticación"""

from datetime import datetime, timedelta
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.config import get_settings

config = get_settings()

# Contexto de criptografía para contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hashea una contraseña"""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica una contraseña contra su hash"""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Crea un token JWT de acceso"""
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=config.access_token_expire_minutes
        )

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, config.secret_key, algorithm=config.algorithm
    )
    return encoded_jwt


def create_refresh_token(data: dict) -> str:
    """Crea un token JWT de refresco"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=config.refresh_token_expire_days)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, config.secret_key, algorithm=config.algorithm
    )
    return encoded_jwt


def decode_token(token: str) -> dict:
    """Decodifica y valida un token JWT"""
    try:
        payload = jwt.decode(token, config.secret_key, algorithms=[config.algorithm])
        return payload
    except JWTError:
        return None
