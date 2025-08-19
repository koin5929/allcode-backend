from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..schemas import VisitedIn
from ..models import Visited
from ..deps import get_db, get_current_user

router = APIRouter(prefix="/visited", tags=["visited"])

@router.post("")
def add_visited(
    data: VisitedIn,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    v = Visited(**data.dict())
    db.add(v)
    try:
        db.commit()
    except Exception:
        db.rollback()  # Unique url_hash 충돌 시 무시
    return {"ok": True}
