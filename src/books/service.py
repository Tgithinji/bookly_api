from sqlmodel.ext.asyncio.session import AsyncSession
from .schemas import CreateBook, UpdateBook
from sqlmodel import select, desc
from .models import Book
from datetime import datetime


class BookService:
    async def get_all_books(self, session:AsyncSession):
        statement = select(Book).order_by(desc(Book.created_at))
        results = await session.exec(statement)
        return results.all()

    async def get_one_books(self, book_id:str, session:AsyncSession):
        statement = select(Book).where(Book.id == book_id)
        result = await session.exec(statement)
        book = result.first()
        return book if book is not None else None

    async def create_book(self, book_data:CreateBook, session:AsyncSession):
        book_dat_dict = book_data.model_dump()
        new_book = Book(**book_dat_dict)
        new_book.published_date = datetime.strptime(book_dat_dict['published_date'], "%Y-%m-%d")
        session.add(new_book)
        await session.commit()
        await session.refresh(new_book)
        return new_book

    async def update_book(self, book_id:str, update_data: UpdateBook, session:AsyncSession):
        book_to_update = await self.get_one_books(book_id, session)
        if book_to_update is None:
            return None
        update_data_dict = update_data.model_dump()
        for key, value in update_data_dict.items():
            setattr(book_to_update, key, value)
        await session.commit()
        await session.refresh(book_to_update)
        return book_to_update

    async def delete_book(self, book_id:str, session:AsyncSession):
        book_to_delete = await self.get_one_books(book_id, session)
        if not book_to_delete:
            return None
        await session.delete(book_to_delete)
        await session.commit()
        return {}
