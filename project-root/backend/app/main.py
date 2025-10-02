# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .settings import settings
from .database import Base, engine, SessionLocal
from .routers import auth as auth_router
from .routers import health as health_router
from .routers import keywords as keywords_router
from .routers import visited as visited_router
from .routers import proxy as proxy_router

# 초기 개발 편의를 위해 자동 생성 (운영에선 Alembic 권장)
# 건들면 안되기 때문에 체크 O ㅇㅇ
Base.metadata.create_all(bind=engine)

# === 여기부터: 최초 관리자 부트스트랩 ===
import os
from .models import User
from .security import hash_password

def _maybe_bootstrap_admin():
    """
    BOOTSTRAP_ADMIN=1 이고, ADMIN_EMAIL/ADMIN_PASSWORD 가 설정돼 있으면
    관리자 계정을 1회성으로 생성합니다.
    """
    if os.getenv("BOOTSTRAP_ADMIN") != "1":
        return

    email = os.getenv("ADMIN_EMAIL")
    password = os.getenv("ADMIN_PASSWORD")
    if not email or not password:
        print("[bootstrap] ADMIN_EMAIL/ADMIN_PASSWORD 미설정 → 건너뜀")
        return

    db = SessionLocal()
    try:
        exists = db.query(User).filter(User.email == email).first()
        if exists:
            print(f"[bootstrap] 이미 존재: {email} → 생성 안 함")
            return
        u = User(email=email, pw_hash=hash_password(password), role="ADMIN", is_active=True)
        db.add(u)
        db.commit()
        print(f"[bootstrap] ✅ 관리자 생성: {email}")
    except Exception as e:
        db.rollback()
        print(f"[bootstrap] 관리자 생성 실패: {e}")
    finally:
        db.close()

_maybe_bootstrap_admin()
# === 여기까지 ===

app = FastAPI(title=settings.APP_NAME)

origins = [o.strip() for o in settings.ALLOWED_ORIGINS.split(",")] if settings.ALLOWED_ORIGINS else ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router.router)
app.include_router(auth_router.router)
app.include_router(keywords_router.router)
app.include_router(visited_router.router)
app.include_router(proxy_router.router)

@app.get("/")
def root():
    return {"name": settings.APP_NAME, "env": settings.ENV}





