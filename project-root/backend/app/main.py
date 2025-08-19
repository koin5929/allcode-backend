from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .settings import settings
from .database import Base, engine
from .routers import auth as auth_router
from .routers import health as health_router
from .routers import keywords as keywords_router
from .routers import visited as visited_router
from .routers import proxy as proxy_router

# 초기 개발 편의를 위해 자동 생성 (운영에선 Alembic 권장)
Base.metadata.create_all(bind=engine)

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
