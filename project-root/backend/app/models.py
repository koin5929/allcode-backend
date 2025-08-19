from sqlalchemy import String, Integer, DateTime, Text, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from .database import Base

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    pw_hash: Mapped[str] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(String(32), default="OPERATOR")  # ADMIN/OPERATOR/VIEWER
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class KeywordProfile(Base):
    __tablename__ = "keyword_profiles"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True)
    keywords: Mapped[str] = mapped_column(Text)  # 줄바꿈 또는 콤마 구분
    freshness_days: Mapped[int] = mapped_column(Integer, default=7)
    daily_limit: Mapped[int] = mapped_column(Integer, default=20)
    blacklist: Mapped[str] = mapped_column(Text, default="")
    whitelist: Mapped[str] = mapped_column(Text, default="")
    created_by: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))

class Visited(Base):
    __tablename__ = "visited"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    url_hash: Mapped[str] = mapped_column(String(64), index=True)
    url: Mapped[str] = mapped_column(Text)
    author: Mapped[str] = mapped_column(String(255), default="")
    posted_at: Mapped[datetime | None]
    ttl_expires_at: Mapped[datetime]
    __table_args__ = (UniqueConstraint("url_hash", name="uq_visited_url_hash"),)

class Candidate(Base):
    __tablename__ = "candidates"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    url: Mapped[str] = mapped_column(Text)
    title: Mapped[str] = mapped_column(Text)
    author: Mapped[str] = mapped_column(String(255), default="")
    posted_at: Mapped[datetime | None]
    quality_score: Mapped[int] = mapped_column(Integer, default=0)
    status: Mapped[str] = mapped_column(String(32), default="QUEUED")  # QUEUED/APPROVED/DONE/FAILED

class Comment(Base):
    __tablename__ = "comments"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    candidate_id: Mapped[int] = mapped_column(Integer, ForeignKey("candidates.id"))
    draft: Mapped[str] = mapped_column(Text)
    final_text: Mapped[str | None]
    approved_by: Mapped[int | None]
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    actor_id: Mapped[int | None]
    action: Mapped[str] = mapped_column(String(64))
    target: Mapped[str] = mapped_column(String(255))
    meta: Mapped[str] = mapped_column(Text, default="")
    ts: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
