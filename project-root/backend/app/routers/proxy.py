import os
from fastapi import APIRouter, Depends
from datetime import datetime, timedelta
from ..schemas import ProxyLeaseOut
from ..deps import get_current_user

router = APIRouter(prefix="/proxy", tags=["proxy"])

@router.post("/lease", response_model=ProxyLeaseOut)
def lease_proxy(user = Depends(get_current_user)):
    # Render 환경변수에서 DataImpulse 값 불러오기
    proxy_host = os.getenv("PROXY_HOST", "gw.dataimpulse.com")
    proxy_port = int(os.getenv("PROXY_PORT", "823"))
    proxy_user = os.getenv("PROXY_USERNAME")
    proxy_pass = os.getenv("PROXY_PASSWORD")

    # 인증 문자열 조합
    auth = f"{proxy_user}:{proxy_pass}" if proxy_user and proxy_pass else None

    return ProxyLeaseOut(
        ip=proxy_host,
        port=proxy_port,
        auth=auth,
        sticky_key=None,
        expires_at=datetime.utcnow() + timedelta(minutes=10),
    )

@router.post("/release")
def release_proxy(user = Depends(get_current_user)):
    return {"ok": True}
