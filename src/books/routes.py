from fastapi import APIRouter, status, HTTPException
from src.books.book_data import books
from src.books.schemas import Book, UpdateBook
from typing import List

book_router = APIRouter()


@book_router.get("/", response_model=List[Book])
async def get_all_books():
  return books


@book_router.get("/{book_id}")
async def get_one_books(book_id: int) -> dict:
  for book in books:
    if book['id'] == book_id:
      return book
  raise HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Book not found")


@book_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_book(book_data: Book) -> dict:
  new_book = book_data.model_dump()
  books.append(new_book)
  return new_book


@book_router.patch("/{book_id}")
async def update_book(book_id: int, update_data: UpdateBook) -> dict:
  for book in books:
    if book['id'] == book_id:
      book.update(update_data.model_dump())
      return book
  
  raise HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Book not found")


@book_router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int):
  for book in books:
    if book['id'] == book_id:
      books.remove(book)
      return
  
  raise HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Book not found")
