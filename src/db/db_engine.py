from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlalchemy import text
from src.config import Config


engine: AsyncEngine = create_async_engine(
    url=Config.DATABASE_URL,
    echo=True
)


async def init_db():
    async with engine.begin() as conn:
        from src.books.models import Book
        
        await conn.run_sync(SQLModel.metadata.create_all)
