from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from backend.database.database import get_db
from backend.models import user_model
from backend.services import token_service, auth_service

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")  # Our login endpoint

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = token_service.decode_access_token(token)
        if payload is None:
            raise credentials_exception
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = auth_service.get_user_by_username(db, username=username)
    if user is None:
        raise credentials_exception
    return user