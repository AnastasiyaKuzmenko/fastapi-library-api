from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import DeclarativeBase, relationship, Mapped, mapped_column
from typing import Optional
from datetime import datetime

class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False) 


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    author: Mapped[str] = mapped_column(nullable=False)
    publication_year: Mapped[Optional[int]] = mapped_column(nullable=True)
    isbn: Mapped[Optional[str]] = mapped_column(unique=True, nullable=True)
    copies_available: Mapped[int] = mapped_column(default=1)

    borrowed_books: Mapped[list["BorrowedBook"]] = relationship(back_populates="book")



class Reader(Base):
    __tablename__ = "readers"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)

    borrowed_books: Mapped[list["BorrowedBook"]] = relationship(back_populates="reader")



class BorrowedBook(Base):
    __tablename__ = "borrowed_books"

    id: Mapped[int] = mapped_column(primary_key=True)
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"))
    reader_id: Mapped[int] = mapped_column(ForeignKey("readers.id"))
    borrowed_date: Mapped[datetime] = mapped_column(default=datetime.utcnow) # check
    return_date: Mapped[Optional[datetime]] = mapped_column(nullable=True)

    book: Mapped["Book"] = relationship(back_populates="borrowed_books")
    reader: Mapped["Reader"] = relationship(back_populates="borrowed_books")


