from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

# ---------------------------
# Users
# ---------------------------


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr

    model_config = {
        "from_attributes": True
    }


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    email: str | None = None

# ---------------------------
# Books
# ---------------------------


class BookCreate(BaseModel):
    title: str
    author: str
    publication_year: Optional[int] = None
    isbn: Optional[str] = None
    copies_available: int = Field(default=1, ge=0)
    description: Optional[str] = None


class BookUpdate(BaseModel):
    title: str
    author: str
    publication_year: Optional[int] = None
    isbn: Optional[str] = None
    copies_available: int = Field(default=1, ge=0)
    description: Optional[str] = None


class BookOut(BaseModel):
    id: int
    title: str
    author: str
    publication_year: Optional[int] = None
    isbn: Optional[str] = None
    copies_available: int
    description: Optional[str] = None

    model_config = {
        "from_attributes": True
    }

# ---------------------------
# Readers
# ---------------------------


class ReaderCreate(BaseModel):
    name: str
    email: EmailStr


class ReaderUpdate(BaseModel):
    name: str
    email: EmailStr


class ReaderOut(BaseModel):
    id: int
    name: str
    email: EmailStr

    model_config = {
        "from_attributes": True
    }

# ---------------------------
# BooksBorrowedBooks
# ---------------------------


class BorrowCreate(BaseModel):
    book_id: int
    reader_id: int


class BorrowOut(BaseModel):
    id: int
    book_id: int
    reader_id: int
    borrow_date: datetime
    return_date: Optional[datetime] = None

    model_config = {
        "from_attributes": True
    }


# ---------------------------
# List of books borrowed by the reader
# ---------------------------

class ReaderBorrowedBook(BaseModel):
    book: BookOut
    borrow_date: datetime

    model_config = {
        "from_attributes": True
    }
