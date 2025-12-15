from sqlmodel import SQLModel, Field
from sqlalchemy import Column
import sqlalchemy.dialects.postgresql as pg
from datetime import datetime, date, timezone
import uuid


class Book(SQLModel, table=True):
    __tablename__ = "books"

    id: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            primary_key=True,
            nullable=False,
            default=uuid.uuid4
        )
    )
    title: str = Field(max_length=255, index=True)
    author: str = Field(max_length=255)
    publisher: str = Field(max_length=255)
    published_date: date
    page_count: int
    language: str = Field(max_length=10)
    created_at: datetime = Field(
        sa_column=Column(
            pg.TIMESTAMP,
            nullable=False,
            default=lambda: datetime.now()
        )
    )

    updated_at: datetime = Field(
        sa_column=Column(
            pg.TIMESTAMP,
            nullable=False,
            default=lambda: datetime.now(),
            onupdate=lambda: datetime.now()
        )
    )

    def __repr__(self):
        return f"<Book title={self.title}>"
