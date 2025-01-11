import os
import jwt
from fastapi import APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import HTTPException, Depends
from datetime import datetime, timedelta
from typing import List, Optional
from dotenv import load_dotenv

from schema import Token

router = APIRouter(
    prefix="/login",
    tags=["LoginOperation"]
)


load_dotenv('dev.env')

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
ACCESS_PASSWORD = str(os.getenv("ACCESS_PASSWORD"))


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/")


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@router.post("/", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.username == "admin" and form_data.password == ACCESS_PASSWORD:
        access_token = create_access_token({"sub": "admin"})
        return {"access_token": access_token, "token_type": "bearer"}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")