import jwt
from datetime import datetime, timedelta
from fastapi import Depends, status, HTTPException , Header
from fastapi.security import OAuth2PasswordBearer
from app.models.user import User
from app.database import *
from app.schemas.user import *
from sqlalchemy.orm import Session
from app.config import settings


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='user')

# SECRET_KEY
# Algorithm
# Expriation time

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
REFRESH_TOKEN_EXPIRE_DAYS = settings.REFRESH_TOKEN_EXPIRE_DAYS


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def create_refresh_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str, credentials_exception):

    try:

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")
        if id is None:
            raise credentials_exception
        token_data = TokenData(id=id)
        return token_data
    
    except HTTPException as error:
        raise error

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired"
        )

    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token"
        )

    except Exception as e:
        raise e




def get_current_user(token: str =  Header(...)):
    try:
        with DBFactory() as db:
            credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                                detail=f"Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})

            token = verify_access_token(token, credentials_exception)

            user = db.query(User).filter(User.id == token.id).first()

            return user
        
    
    except HTTPException as error:
        raise error

    # Step 7: Handle unexpected errors
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error)
        ) from error

def create_reset_token(data: dict):
    to_encode = data.copy()

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt  


def refresh_access_token(refresh_token: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("user_id")
        if user_id is None:
            raise credentials_exception

        with DBFactory() as db:
            user = db.query(User).filter(User.id == user_id).first()
            if user is None:
                raise credentials_exception

        new_access_token = create_access_token(data={"user_id": user.id, "role": user.role, "name": user.username, "email_id": user.email})
        return new_access_token
    except jwt.PyJWTError:
        raise credentials_exception
