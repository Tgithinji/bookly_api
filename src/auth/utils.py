from passlib.context import CryptContext
from datetime import timedelta, datetime, timezone
from src.config import Config
import jwt
import uuid
import logging


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def generate_password_hash(plain_password: str) -> str:
    return pwd_context.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(user_data:dict, expiry: timedelta = None, refresh: bool = False):
    payload = user_data.copy()
    
    now = datetime.now(timezone.utc)

    if expiry is not None:
        expire = now + expiry
    elif refresh:
        expire = now + timedelta(days=7)
    else:
        expire = now + timedelta(minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES)

    payload.update({
            "sub": str(user_data.get("user_id")),
            "exp": expire,
            "jti": str(uuid.uuid4()),
            "refresh": refresh
    })
    
    access_token = jwt.encode(
        payload=payload,
        key=Config.JWT_SECRET,
        algorithm=Config.JWT_ALGORITHM
    )
    
    return access_token


def decode_token(token: str) -> dict:
    try:
        token_data = jwt.decode(
            jwt=token,
            key=Config.JWT_SECRET,
            algorithms=[Config.JWT_ALGORITHM]
        )
        return token_data
    
    except jwt.ExpiredSignatureError:
        logging.warning("Token has expired")
        return None
    
    except jwt.InvalidTokenError as e:
        logging.exception(e)
        return None
    