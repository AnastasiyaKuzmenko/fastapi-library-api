from fastapi import APIRouter, Depends, HTTPException
from app import schemas, models, auth
from sqlalchemy.orm import Session

from ..dependencies import get_db

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get("/register", response_model=schemas.UserOut)
async def register_users(user_data: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.email == user_data.email).first()
    if existing_user:
            raise HTTPException(
            status_code=400,
            detail="User with this email already exist"
        )
    user_hashed_password = auth.get_password_hash(user_data.password)

    new_user = models.User(email=user_data.email, hashed_password=user_hashed_password)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user