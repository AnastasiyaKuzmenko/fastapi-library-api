from fastapi import APIRouter, Depends, HTTPException
from ..dependencies import get_db, get_current_user
from sqlalchemy.orm import Session
from app import models, schemas
from datetime import datetime

router = APIRouter(
    prefix="/borrow",
    tags=["Borrow"]
)


@router.post("/return", response_model=schemas.BorrowOut)
def return_book(
    borrow_data: schemas.BookCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    
    borrow_record = db.query(models.BorrowedBook).filter(
        models.BorrowedBooks.book_id == borrow_data.book_id,
        models.BorrowedBooks.reader_id == borrow_data.reader_id,
        models.BorrowedBooks.return_date == None
    ).first()
    if not borrow_record:
        raise HTTPException(
            status_code=400,
            detail="This book is not currently borrowed by this reader"
        )

    borrow_record.return_date = datetime.utcnow()

    book = db.query(models.Book).filter(models.Book.id == borrow_data.book_id).first()
    if book:
        book.copies_available += 1
    else:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )
    
    db.commit()
    db.refresh(borrow_record)
    return borrow_record