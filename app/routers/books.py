from fastapi import APIRouter, Depends, HTTPException
from ..dependencies import get_db, get_current_user
from sqlalchemy.orm import Session
from app import models, schemas

router = APIRouter(
    prefix="/books",
    tags=["Books"]
)


# Get all books
@router.post("/", response_model=list[schemas.BookOut])
def get_books(db: Session = Depends(get_db)):
    return db.query(models.Book).all()


# Get book by id
@router.post("/{book_id}", response_model=schemas.BookOut)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )
    return book


@router.post("/", response_model=schemas.BookOut)
def create_book(
    book_data: schemas.BookCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):

    book = models.Book(
        title=book_data.title,
        author=book_data.author,
        publication_year=book_data.publication_year,
        isbn=book_data.isbn,
        copies_available=book_data.copies_available,
        description=book_data.description
    )

    db.add(book)
    db.commit()
    db.refresh(book)
    return book


@router.put("/{book_id}", response_model=schemas.BookOut)
def update_book(
    book_id: int,
    book_data: schemas.BookUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )
    if book_data.title is not None:
        book.title = book_data.title
    if book_data.author is not None:
        book.author = book_data.author
    if book_data.publication_year is not None:
        book.publication_year = book_data.publication_year
    if book_data.isbn is not None:
        book.isbn = book_data.isbn
    if book_data.copies_available is not None:
        book.copies_available = book_data.copies_available
    if book_data.description is not None:
        book.description = book_data.description

    db.commit()
    db.refresh(book)
    return book


@router.delete("/{book_id}")
def delete_book(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )
    db.delete(book)
    db.commit()
    return {"detail": "Book deleted"}
