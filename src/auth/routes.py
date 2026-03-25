from fastapi import APIRouter, status, HTTPException, Depends
from .schemas import UserCreate, User, UserLogin
from .service import AuthService
from src.db.db_engine import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from .utils import create_access_token, decode_token, verify_password
from fastapi.responses import JSONResponse


auth_router = APIRouter()
auth_service = AuthService()


@auth_router.post('/signup', response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    session: AsyncSession = Depends(get_session)
):
    email = user_data.email
    existing_user = await auth_service.get_user_by_email(email, session)
    if existing_user is not None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User already exists"
        )
    new_user = await auth_service.create_user(user_data, session)

    return new_user


@auth_router.post('/login')
async def login_user(
    login_data: UserLogin,
    session: AsyncSession = Depends(get_session)
):
    user = await auth_service.get_user_by_email(login_data.email, session)
    if user is None or not verify_password(login_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    access_token = create_access_token(
        user_data={"user_id": str(user.id), "email": user.email},
    )

    refresh_token = create_access_token(
        user_data={"user_id": str(user.id), "email": user.email},
        refresh=True
    )

    return JSONResponse(
        content={
            "message": "Login successful",
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "user":{
                "id": str(user.id),
                "email": user.email,
                "username": user.username
            }
        }
    )