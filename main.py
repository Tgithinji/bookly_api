from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()


books = [
  {
    "id": 1,
    "title": "The Silent Code",
    "author": "Ethan Brooks",
    "publisher": "TechLeaf Press",
    "published_date": "2019-04-15",
    "page_count": 320,
    "language": "English"
  },
  {
    "id": 2,
    "title": "Beyond the Horizon",
    "author": "Lina Mwangi",
    "publisher": "Sunrise Publications",
    "published_date": "2021-08-02",
    "page_count": 278,
    "language": "English"
  },
  {
    "id": 3,
    "title": "Artificial Minds",
    "author": "Dr. Paul Kim",
    "publisher": "FutureWorks",
    "published_date": "2022-01-10",
    "page_count": 412,
    "language": "English"
  },
  {
    "id": 4,
    "title": "Shadows of Nairobi",
    "author": "James Otieno",
    "publisher": "Savannah House",
    "published_date": "2018-06-21",
    "page_count": 245,
    "language": "English"
  },
  {
    "id": 5,
    "title": "The Last Voyage",
    "author": "Isabella Cruz",
    "publisher": "BlueWave Books",
    "published_date": "2020-11-05",
    "page_count": 356,
    "language": "English"
  },
  {
    "id": 6,
    "title": "Startup to Scale",
    "author": "Michael Trent",
    "publisher": "GrowthLab Media",
    "published_date": "2023-03-18",
    "page_count": 198,
    "language": "English"
  },
  {
    "id": 7,
    "title": "Whispers of the Past",
    "author": "Amina Hassan",
    "publisher": "Golden Pen Publishing",
    "published_date": "2017-09-12",
    "page_count": 301,
    "language": "English"
  },
  {
    "id": 8,
    "title": "Learning Python the Hard Way",
    "author": "Robert Meyers",
    "publisher": "CodeCraft Press",
    "published_date": "2021-02-27",
    "page_count": 450,
    "language": "English"
  },
  {
    "id": 9,
    "title": "Designing Better APIs",
    "author": "Sophia Nguyen",
    "publisher": "DevSphere",
    "published_date": "2022-10-14",
    "page_count": 289,
    "language": "English"
  },
  {
    "id": 10,
    "title": "The Art of Focus",
    "author": "Daniel Roth",
    "publisher": "Mindful Reads",
    "published_date": "2016-05-30",
    "page_count": 214,
    "language": "English"
  }
]


class Book(BaseModel):
    id: int
    title: str
    author: str
    publisher: str
    published_date: str
    page_count: int
    language: str


class UpdateBook(BaseModel):
    title: str
    author: str
    publisher: str
    page_count: int
    language: str


@app.get("/books", response_model=List[Book])
async def get_all_books():
  return books


@app.get("/books/{book_id}")
async def get_one_books(book_id: int) -> dict:
  for book in books:
    if book['id'] == book_id:
      return book
  raise HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Book not found")


@app.post("/books", status_code=status.HTTP_201_CREATED)
async def create_book(book_data: Book) -> dict:
  new_book = book_data.model_dump()
  books.append(new_book)
  return new_book


@app.patch("/books/{book_id}")
async def update_book(book_id: int, update_data: UpdateBook) -> dict:
  for book in books:
    if book['id'] == book_id:
      book.update(update_data.model_dump())
      return book
  
  raise HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Book not found")


@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int):
  for book in books:
    if book['id'] == book_id:
      books.remove(book)
      return
  
  raise HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Book not found")
