from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from .. import models, schemas
from ..auth import create_access_token, hash_password, verify_password
from ..database import get_db
from ..dependencies import get_current_user


router = APIRouter(prefix="/auth", tags=["Users / Authentication"])


@router.post("/register", response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED)
def register(data: schemas.UserCreate, db: Session = Depends(get_db)):
    email = data.email.lower()
    username = data.username.lower()
    if db.scalar(select(models.User).where(models.User.email == email)):
        raise HTTPException(status_code=400, detail="Bu e-posta zaten kayıtlı.")
    if db.scalar(select(models.User).where(models.User.username == username)):
        raise HTTPException(status_code=400, detail="Bu kullanıcı adı zaten alınmış.")
    user = models.User(
        name=data.name,
        username=username,
        email=email,
        hashed_password=hash_password(data.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/login", response_model=schemas.Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    # OAuth2 formundaki "username" alanında gerçek kullanıcı adı kullanılır.
    user = db.scalar(
        select(models.User).where(models.User.username == form_data.username.lower())
    )
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Kullanıcı adı veya şifre hatalı.")
    return schemas.Token(access_token=create_access_token(user.id))


@router.get("/me", response_model=schemas.UserOut)
def me(current_user: models.User = Depends(get_current_user)):
    return current_user
