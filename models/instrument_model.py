from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Float
from sqlalchemy.orm import relationship
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from database import Base
from datetime import datetime

from models.user_model import User


# ---------- SQLAlchemy Models ----------
class InstrumentDB(Base):
    __tablename__ = "instruments"

    # id
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    # user
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    
    cost = Column(Float, nullable=False)
    amortization = Column(Float, nullable=False)
    maintenance_cost = Column(Float, nullable=False)
    # service columns
    created_at = Column(DateTime(timezone=True), default=datetime.now, nullable=True)
    created_by = Column(String, nullable=True, default="System")
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.now, nullable=True)
    updated_by = Column(String, nullable=True)

    # relationships
    user = relationship("UserDB", back_populates="instruments", lazy="selectin")

# ---------- Pydantic Schemas ----------
class Instrument(BaseModel):
    # id
    id: Optional[int] = None
    # user
    user_id: int

    name: str = Field(
        ...,
        min_length=2,
        max_length=50,
        description="Name must be between 2 and 50 characters",
    )
    description: Optional[str] = None
    cost: float = Field(..., ge=0, description="The cost must be greater than zero")
    amortization: float = Field(..., ge=0, description="The amortization cost must be greater than zero")
    maintenance_cost: float = Field(..., ge=0, description="The maintenance cost must be greater than zero")
    # service columns
    created_at: Optional[datetime] = None
    created_by: Optional[str]
    updated_at: Optional[datetime] = None
    updated_by: Optional[str]

    class Config:
        orm_mode = True

class InstrumentWithDetail(Instrument):
    user: User