from typing import Generator
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session
import ast

from app import crud, models, schemas
from app.core.config import settings
from app.core import security
from app.db.session import SessionLocal

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> models.User:
    # print({"token-admin": token})
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY,
                             algorithms=[security.ALGORITHM])
        # print(payload.get("sub"))
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenPayload(sub=username)
    except JWTError:
        # print(f"JWT Token Validation Error: {JWTError}")
        raise credentials_exception

    # Convert the string to a Python dictionary
    token_dict = ast.literal_eval(token_data.sub)
    username = token_dict.get('sub')
    # print({"token-data": token_data.sub,
    #       "type-object": type(token_data.sub), 'dict-username': username})
    user = crud.user.get_by_username(db, username=username)
    # get(db, username=token_data.sub)
    # print(user)
    if user is None:
        raise credentials_exception
    return user


def get_current_authenticated_user(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    if not crud.user.is_authenticated(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't authenticated")
    return current_user


def get_current_active_superuser(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    if not crud.user.is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user
