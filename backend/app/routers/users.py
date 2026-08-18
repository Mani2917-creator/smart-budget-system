from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas, auth
from app.database import get_db


router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@router.post("/register")
def register(
    user: schemas.UserCreate,
    db: Session = Depends(get_db)
):
    existing = (
        db.query(models.User)
        .filter(models.User.email == user.email)
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    new_user = models.User(
        name=user.name,
        email=user.email,
        hashed_password=auth.hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "msg": "registered",
        "user_id": new_user.id
    }


@router.post("/login", response_model=schemas.Token)
def login(
    user: schemas.UserLogin,
    db: Session = Depends(get_db)
):
    db_user = (
        db.query(models.User)
        .filter(models.User.email == user.email)
        .first()
    )

    if not db_user or not auth.verify_password(
        user.password,
        db_user.hashed_password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    token = auth.create_access_token(
        {"sub": str(db_user.id)}
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }