from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..schemas import KeywordProfileIn, KeywordProfileOut
from ..models import KeywordProfile
from ..deps import get_db, get_current_user

router = APIRouter(prefix="/keywords", tags=["keywords"])

@router.post("/profiles", response_model=KeywordProfileOut)
def create_profile(
    data: KeywordProfileIn,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    if db.query(KeywordProfile).filter(KeywordProfile.name == data.name).first():
        raise HTTPException(status_code=400, detail="Profile name exists")
    prof = KeywordProfile(**data.dict(), created_by=user.id)
    db.add(prof)
    db.commit()
    db.refresh(prof)
    return prof

@router.get("/profiles", response_model=list[KeywordProfileOut])
def list_profiles(db: Session = Depends(get_db), user = Depends(get_current_user)):
    return db.query(KeywordProfile).all()
