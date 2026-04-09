from sqlalchemy import JSON, DateTime, Integer, String, event, func
from sqlalchemy.orm import Mapped, declarative_base, mapped_column
from datetime import datetime
from dateutil import tz
from ..extensions import db
from pydantic import BaseModel, Field
from typing import List, Optional

# TODO: et faire upload des images
class Build(db.Model):
    __tablename__ = 'builds'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    author: Mapped[str] = mapped_column(String, nullable=False)
    
    images: Mapped[List[str]] = mapped_column(JSON, default=list)
    
    created: Mapped[str] = mapped_column(DateTime, server_default=func.now())
    modified: Mapped[str] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

class BuildSchema(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    description: str = Field(..., min_length=10)
    author: str = Field(..., min_length=3, max_length=18)
    
    images: List[str] = Field(default_factory=list, description="Liste des noms de fichiers")
    
    created: Optional[str] = None
    modified: Optional[str] = None

    class Config:
        from_attributes = True