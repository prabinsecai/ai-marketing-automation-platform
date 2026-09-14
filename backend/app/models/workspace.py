import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, Text, JSON
from sqlalchemy.orm import relationship
from app.database import Base


class Workspace(Base):
    __tablename__ = "workspaces"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), nullable=False)
    slug = Column(String(255), unique=True, nullable=False, index=True)
    industry = Column(String(100), nullable=True)
    website = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    brand_guidelines = Column(Text, nullable=True)  # Voice, tone, keywords, constraints
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    users = relationship("User", back_populates="workspace", cascade="all, delete-orphan")
    products = relationship("Product", back_populates="workspace", cascade="all, delete-orphan")
    audiences = relationship("Audience", back_populates="workspace", cascade="all, delete-orphan")
    campaigns = relationship("Campaign", back_populates="workspace", cascade="all, delete-orphan")
    approvals = relationship("Approval", back_populates="workspace", cascade="all, delete-orphan")
    ai_logs = relationship("AILog", back_populates="workspace", cascade="all, delete-orphan")
