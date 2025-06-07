from fastapi import APIRouter, Depends, HTTPException
from ..dependencies import get_db, get_current_user
from sqlalchemy.orm import Session
from app import models, schemas

router = APIRouter(
    prefix="/readers",
    tags=["Readers"]
)


# Get all readers
@router.get("/", response_model=list[schemas.ReaderOut])
def get_readers(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return db.query(models.Reader).all()


# Get reader by id
@router.get("/{reader_id}", response_model=schemas.ReaderOut)
def get_reader(
    reader_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    reader = db.query(models.Reader).filter(models.Reader.id == reader_id).first()
    if not reader:
        raise HTTPException(
            status_code=404,
            detail="Reader not found"
        )
    return reader


@router.post("/", response_model=schemas.ReaderOut)
def create_reader(
    reader_data: schemas.ReaderCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):

    reader = models.Reader(
        name=reader_data.name,
        email=reader_data.email
    )

    db.add(reader)
    db.commit()
    db.refresh(reader)
    return reader


@router.put("/{reader_id}", response_model=schemas.ReaderOut)
def update_reader(
    reader_id: int,
    reader_data: schemas.ReaderUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    reader = db.query(models.Reader).filter(models.Reader.id == reader_id).first()
    if not reader:
        raise HTTPException(
            status_code=404,
            detail="Reader not found"
        )
    if reader_data.name is not None:
        reader.name = reader_data.name
    if reader_data.email is not None:
        reader.email = reader_data.email

    db.commit()
    db.refresh(reader)
    return reader


@router.delete("/{reader_id}")
def delete_reader(
    reader_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    reader = db.query(models.Reader).filter(models.Reader.id == reader_id).first()
    if not reader:
        raise HTTPException(
            status_code=404,
            detail="Reader not found"
        )
    db.delete(reader)
    db.commit()
    return {"detail": "Reader deleted"}
