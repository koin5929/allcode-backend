from fastapi import APIRouter, Depends
from datetime import datetime, timedelta
from ..schemas import ProxyLeaseOut
from ..deps import get_current_user

router = APIRouter(prefix="/proxy", tags=["proxy"])

@router.post("/lease", response_model=ProxyLeaseOut)
def lease_proxy(user = Depends(get_current_user)):
    # 실제 구현에서는 공급자 API 호출 및 헬스/스코어링 적용
    return ProxyLeaseOut(
        ip="127.0.0.1",
        port=8080,
        auth=None,
        sticky_key=None,
        expires_at=datetime.utcnow() + timedelta(minutes=10),
    )

@router.post("/release")
def release_proxy(user = Depends(get_current_user)):
    return {"ok": True}
