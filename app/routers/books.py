from fastapi import APIRouter, Depends, HTTPException
from ..dependencies import get_db, get_current_user
from sqlalchemy.orm import Session
from app import models

router = APIRouter(
    prefix="/books",
    tags=["Books"]
)

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

