from fastapi import APIRouter, status, HTTPException, Depends
from src.books.schemas import Book, UpdateBook, CreateBook
from typing import List
from src.db.db_engine import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from .service import BookService


book_router = APIRouter()
book_service = BookService()


@book_router.get("/", response_model=List[Book])
async def get_all_books(session:AsyncSession = Depends(get_session)):
  books = await book_service.get_all_books(session)
  return books


@book_router.get("/{book_id}", response_model=Book)
async def get_one_books(book_id:str, session:AsyncSession = Depends(get_session)) -> dict:
  book = await book_service.get_one_books(book_id, session)
  if book is None:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail="Book not found")
  return book


@book_router.post("/", status_code=status.HTTP_201_CREATED, response_model=Book)
async def create_book(book_data: CreateBook, session:AsyncSession = Depends(get_session)) -> dict:
  new_book = await book_service.create_book(book_data, session)
  return new_book


@book_router.patch("/{book_id}", status_code=status.HTTP_201_CREATED, response_model=Book)
async def update_book(
    book_id:str,
    update_data: UpdateBook,
    session:AsyncSession = Depends(get_session)
) -> dict:
    updated_book = await book_service.update_book(book_id, update_data, session)
    if updated_book is None:
      raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Book not found"
      )
    return updated_book


@book_router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id:str, session:AsyncSession = Depends(get_session)):
    deleted_book = await book_service.delete_book(book_id, session)
    if deleted_book is None:
      raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Book not found"
      )
    