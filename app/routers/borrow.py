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
    borrow_data: schemas.BorrowCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):

    borrow_record = db.query(models.BorrowedBook).filter(
        models.BorrowedBook.book_id == borrow_data.book_id,
        models.BorrowedBook.reader_id == borrow_data.reader_id,
        models.BorrowedBook.return_date == None
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


@router.post("/checkout", response_model=schemas.BorrowOut)
def checkout_book(
    borrow_data: schemas.BorrowCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):

    book = db.query(models.Book).filter(models.Book.id == borrow_data.book_id).first()
    if not book:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    if book.copies_available < 1:
        raise HTTPException(status_code=400, detail="No copies available to borrow")

    reader = db.query(models.Reader).filter(models.Reader.id == borrow_data.reader_id).first()
    if not reader:
        raise HTTPException(
            status_code=404,
            detail="Reader not found"
        )

    active_borrows_count = db.query(models.BorrowedBook).filter(
        models.BorrowedBook.reader_id == borrow_data.reader_id,
        models.BorrowedBook.return_date == None
    ).count()

    if active_borrows_count >= 3:
        raise HTTPException(
            status_code=400,
            detail="Reader already has 3 borrowed books"
        )

    borrow_record = models.BorrowedBooks(
        book_id=borrow_data.book_id,
        reader_id=borrow_data.reader_id,
        borrow_date=datetime.utcnow(),
        return_date=None
    )

    book.copies_available -= 1

    db.add(borrow_record)
    db.commit()
    db.refresh(borrow_record)
    return borrow_record


@router.get("/reader/{reader_id}", response_model=list[schemas.BorrowOut])
def get_active_borrows_for_reader(
    reader_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    borrows = db.query(models.BorrowedBook).filter(
        models.BorrowedBook.reader_id == reader_id,
        models.BorrowedBook.return_date == None
    ).all()

    return borrows
