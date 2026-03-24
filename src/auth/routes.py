from fastapi import APIRouter, status, HTTPException, Depends
from .schemas import UserCreate, User
from .service import AuthService
from src.db.db_engine import get_session
from sqlmodel.ext.asyncio.session import AsyncSession


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
