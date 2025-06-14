from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select

from fastapi_zero.database import AsyncSession, get_session
from fastapi_zero.models import User
from fastapi_zero.schemas import (
    Token,
)
from fastapi_zero.security import (
    create_access_token,
    verify_password,
)

router = APIRouter(prefix='/auth', tags=['auth'])
Session = Annotated[AsyncSession, Depends(get_session)]
OAuthFrom = Annotated[OAuth2PasswordRequestForm, Depends()]


@router.post('/token', response_model=Token)
async def login_for_access_token(
    form_data: OAuthFrom,
    session: Session,  # type: ignore
):
    user = await session.scalar(
        select(User).where(User.email == form_data.username)
    )

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Incorrect Email or Password!',
        )
    if not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Incorrect Email or Password!',
        )

    access_token = create_access_token(data={'sub': user.email})

    return {'access_token': access_token, 'token_type': 'bearer'}
