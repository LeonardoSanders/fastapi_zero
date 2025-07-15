from datetime import datetime, timedelta
from http import HTTPStatus
from zoneinfo import ZoneInfo

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import (  # type: ignore
    DecodeError,
    ExpiredSignatureError,
    decode,
    encode,
)
from pwdlib import PasswordHash  # type: ignore
from sqlalchemy import select

from fastapi_zero.database import AsyncSession, get_session
from fastapi_zero.models import User
from fastapi_zero.settings import Settings

pwd_context = PasswordHash.recommended()
settings = Settings()  # type: ignore
oauth2_schema = OAuth2PasswordBearer(tokenUrl='auth/token')


def get_password_hash(password: str):
    return pwd_context.hash(password)
    # Recebe uma senha em texto simples e a
    # converte em um hash seguro usando


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)
    # Compara uma senha em texto simples fornecida pelo
    # usuário com o hash de senha armazenado no banco de dados


def create_access_token(data: dict):
    to_encode = data.copy()
    # 1. Copia os dados que formarão o payload

    # 2. Calcula o tempo de expiração do token
    expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    # 3. Adiciona a claim 'exp' ao payload
    to_encode.update({'exp': expire})
    encoded_jwt = encode(  # 4. Codifica o JWT
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )

    return encoded_jwt


async def get_current_user(
    session: AsyncSession = Depends(get_session),
    token: str = Depends(oauth2_schema),
):
    """
    Decodifica o token de acesso, valida as credenciais e retorna o usuário.

    - **Args**:
        - `session` (AsyncSession): Sessão de banco de dados injetada.
        - `token` (str): Token JWT extraído do cabeçalho de autorização.

    - **Raises**:
        - `HTTPException(401)`: Se o token for inválido, expirado,
          não contiver o payload esperado ou o usuário não for encontrado.

    - **Returns**:
        - `User`: O objeto do usuário autenticado.
    """
    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )
    try:
        payload = decode(
            token, settings.SECRET_KEY, algorithms=settings.ALGORITHM
        )
        subject_email = payload.get('sub')
        if not subject_email:
            raise credentials_exception

    except DecodeError:
        raise credentials_exception
    except ExpiredSignatureError:
        raise credentials_exception

    user = await session.scalar(
        select(User).where(User.email == subject_email)
    )

    if not user:
        raise credentials_exception

    return user
