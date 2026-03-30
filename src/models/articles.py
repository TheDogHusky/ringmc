from typing import List

from sqlalchemy import Integer, String, event, JSON
from sqlalchemy.orm import declarative_base, mapped_column, validates, Mapped
from datetime import datetime
from dateutil import tz

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
    created = mapped_column(String)
    modified = mapped_column(String)

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

# https://stackoverflow.com/questions/13978554
@event.listens_for(Article, 'before_insert')
def update_created_modified_on_create_listener(mapper, connection, target):
  """ Event listener that runs before a record is updated, and sets the create/modified field accordingly."""
  target.created = datetime.utcnow()
  target.modified = datetime.utcnow()

@event.listens_for(Article, 'before_update')
def update_modified_on_update_listener(mapper, connection, target):
  """ Event listener that runs before a record is updated, and sets the modified field accordingly."""
  target.modified = datetime.now(tz.tzlocal())