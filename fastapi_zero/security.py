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
    session: AsyncSession = Depends(get_session),  # 1
    token: str = Depends(oauth2_schema),  # 2
):
    credentials_exception = HTTPException(  # 3
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )
    try:
        payload = decode(  # 4
            token, settings.SECRET_KEY, algorithms=settings.ALGORITHM
        )
        subject_email = payload.get('sub')  # 5
        if not subject_email:  # 6
            raise credentials_exception

    except DecodeError:  # 7
        raise credentials_exception
    except ExpiredSignatureError:
        raise credentials_exception

    user = await session.scalar(  # 8
        select(User).where(User.email == subject_email)
    )

    if not user:  # 9
        raise credentials_exception

    return user  # 10


"""
1-Injeta uma sessão de banco de dados;
2-Extrai o token do cabeçalho de autorização;
3-Define uma exceção padrão para credenciais inválidas;
4-Decodifica e verifica o token;
5-Obtém o email do payload (claim 'sub');
6-Se não houver email no payload, lança exceção;
7-Captura erros de decodificação/assinatura;
8-Busca o usuário no banco de dados usando o email do payload;
9-Se o usuário não for encontrado (mesmo com token válido), lança exceção
10-Retorna o objeto User;
"""
