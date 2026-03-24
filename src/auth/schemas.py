from pydantic import BaseModel, Field
import uuid
from datetime import datetime


class UserCreate(BaseModel):
    username:str = Field(max_length=10)
    email:str = Field(max_length=40)
    first_name:str = Field(max_length=10)
    last_name:str = Field(max_length=10)
    password:str =  Field(min_length=8)


class User(BaseModel):
    id:uuid.UUID
    username:str
    email:str
    first_name:str
    last_name:str
    is_verified:bool
    created_at:datetime
    updated_at:datetime
