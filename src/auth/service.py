from sqlmodel.ext.asyncio.session import AsyncSession
from .schemas import UserCreate
from sqlmodel import select
from .models import User
from .utils import generate_password_hash


class AuthService:
    async def get_user_by_email(self, email:str, session: AsyncSession):
        statement = select(User).where(User.email == email)
        result = await session.exec(statement)
        user = result.first()
        return user if user is not None else None
    
    async def create_user(self, user_data: UserCreate, session: AsyncSession):
        user_data_dict = user_data.model_dump()
        new_user = User(**user_data_dict)
        new_user.password_hash = generate_password_hash(user_data_dict['password'])

        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return new_user
    