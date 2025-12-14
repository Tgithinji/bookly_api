from fastapi import FastAPI
from src.books.routes import book_router
from contextlib import asynccontextmanager
from src.db.db_engine import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Server starting..")
    await init_db()
    yield
    print("Server shutting down..")


version = "v1"

app = FastAPI(
    title="Book Management API",
    version=version,
    lifespan=lifespan
)


app.include_router(book_router, prefix=f"/api/{version}/books", tags=['books'])
