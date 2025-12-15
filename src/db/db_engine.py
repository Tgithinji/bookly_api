from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
from src.config import Config


engine: AsyncEngine = create_async_engine(
    url=Config.DATABASE_URL,
    echo=True
)


AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def init_db():
    async with engine.begin() as conn:
        from src.books.models import Book

        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session
