from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["health"])

@router.get("/z")
def healthz():
    return {"ok": True}
