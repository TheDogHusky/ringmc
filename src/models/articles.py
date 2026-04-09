from typing import List, Optional

from sqlalchemy import DateTime, Integer, String, event, JSON, func
from sqlalchemy.orm import declarative_base, mapped_column, validates, Mapped
from datetime import datetime
from dateutil import tz
from pydantic import BaseModel, Field

from src.types import PriceEntry
from ..extensions import db

# TODO: finir 
class Article(db.Model):
    __tablename__ = 'articles'
    id = mapped_column(Integer, primary_key=True)
    title = mapped_column(String, nullable=False)
    content = mapped_column(String, nullable=False)
    author = mapped_column(String, nullable=False) # pseudo mc
    # Prices : du troc: on peut mettre une liste de produits à ramener en échange de l'article
    # Dont prices est un tableau de (string, quantité): ("diamant", 3), ..
    prices: Mapped[List[PriceEntry]] = mapped_column(JSON, default=list) # sera serialized en JSON pour stocker la liste des prix possibles pour l'article
    # Image, optionel
    image_url = mapped_column(String, nullable=True)
    # Catégorie, optionel
    category = mapped_column(String, nullable=True)
    # Date de publication, automatique
    created: Mapped[str] = mapped_column(DateTime, server_default=func.now())
    modified: Mapped[str] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    @validates('prices')
    def validate_prices(self, key, prices):
        if not isinstance(prices, list):
            raise ValueError("Prices must be a list")
            
        for entry in prices:
            # Check structure: must have 'item' and 'value'
            if not all(k in entry for k in ("item", "value")):
                raise ValueError("Chaque entrée doit avoir 'item' et 'value'")
            
            # Check types within the JSON
            if not isinstance(entry['item'], str) or not isinstance(entry['value'], int):
                raise TypeError("'item' doit être une chaîne de caractères et 'value' doit être un entier")
                
        return prices

class PriceEntrySchema(BaseModel):
    item: str = Field(..., min_length=1, description="Nom de l'item MC")
    value: int = Field(..., gt=0, description="Quantité (doit être > 0)")

class ArticleSchema(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    content: str = Field(..., min_length=10)
    author: str = Field(..., min_length=3, max_length=18)
    
    prices: List[PriceEntrySchema] = []
    
    # Optional fields
    image_url: Optional[str] = None
    category: Optional[str] = None
    
    created: Optional[str] = None
    modified: Optional[str] = None

    class Config:
        from_attributes = True