import os
import jwt
from fastapi import HTTPException, Depends, Query
from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from dotenv import load_dotenv
from sqlalchemy.orm import Session

from database import get_db
from model import User
from routers.login import oauth2_scheme
from schema import Token, UserCreate, UserResponse, UserUpdate


load_dotenv('dev.env')

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")



router = APIRouter(
    prefix="/user",
    tags=["UserOperation"]
)


def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    if payload.get("sub") != "admin":
        raise HTTPException(status_code=401, detail="Unauthorized")


@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db), token: str = Depends(get_current_user)):
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db), token: str = Depends(get_current_user)):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db), token: str = Depends(get_current_user)):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    for key, value in user_update.dict().items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user


@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: int, db: Session = Depends(get_db), token: str = Depends(get_current_user)):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()


@router.get("/", response_model=List[UserResponse])
def list_users(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    name: Optional[str] = None,
    email: Optional[str] = None,
    db: Session = Depends(get_db),
    token: str = Depends(get_current_user),
):
    query = db.query(User)
    if name:
        query = query.filter(User.name.ilike(f"%{name}%"))
    if email:
        query = query.filter(User.email.ilike(f"%{email}%"))
    users = query.offset((page - 1) * limit).limit(limit).all()
    return users


