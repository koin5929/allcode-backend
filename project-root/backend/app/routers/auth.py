from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..schemas import UserCreate, UserOut, LoginIn, TokenPair
from ..models import User
from ..security import hash_password, verify_password, create_token
from ..deps import get_db
from ..settings import settings

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserOut)
def register(data: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(status_code=400, detail="Email exists")
    user = User(email=data.email, pw_hash=hash_password(data.password), role=data.role)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.post("/login", response_model=TokenPair)
def login(data: LoginIn, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not verify_password(data.password, user.pw_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access = create_token(user.email, minutes=settings.ACCESS_TOKEN_EXPIRES_MIN)
    refresh = create_token(user.email, minutes=60*24*settings.REFRESH_TOKEN_EXPIRES_DAYS)
    return TokenPair(access_token=access, refresh_token=refresh)
