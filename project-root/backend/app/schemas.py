from pydantic import BaseModel, EmailStr
from datetime import datetime

class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: str = "OPERATOR"

class UserOut(BaseModel):
    id: int
    email: EmailStr
    role: str
    is_active: bool
    class Config:
        from_attributes = True

class LoginIn(BaseModel):
    email: EmailStr
    password: str

class KeywordProfileIn(BaseModel):
    name: str
    keywords: str
    freshness_days: int = 7
    daily_limit: int = 20
    blacklist: str = ""
    whitelist: str = ""

class KeywordProfileOut(KeywordProfileIn):
    id: int
    created_by: int
    class Config:
        from_attributes = True

class VisitedIn(BaseModel):
    url: str
    url_hash: str
    author: str = ""
    posted_at: datetime | None = None
    ttl_expires_at: datetime

class ProxyLeaseOut(BaseModel):
    ip: str
    port: int
    auth: str | None = None
    sticky_key: str | None = None
    expires_at: datetime | None = None
