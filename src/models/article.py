from sqlalchemy import Column, Integer, String, event
from sqlalchemy.orm import declarative_base
from datetime import datetime
from dateutil import tz

Base = declarative_base()

# TODO: finir 
class Article(Base):
    __tablename__ = 'articles'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    content = Column(String)
    # Prices : du troc: on peut mettre une liste de produits à ramener en échange de l'article
    # Dont prices est un tableau de (string, quantité): ("diamant", 3), ..
    prices = Column(String) # sera serialized en JSON pour stocker la liste des prix possibles pour l'article
    # Image, optionel
    image_url = Column(String)
    # Catégorie, optionel
    category = Column(String)
    # Date de publication, automatique
    created = Column(String)
    modified = Column(String)

# https://stackoverflow.com/questions/13978554
@event.listen(Article, 'before_insert')
def update_created_modified_on_create_listener(mapper, connection, target):
  """ Event listener that runs before a record is updated, and sets the create/modified field accordingly."""
  target.created = datetime.utcnow()
  target.modified = datetime.utcnow()

@event.listen(Article, 'before_update')
def update_modified_on_update_listener(mapper, connection, target):
  """ Event listener that runs before a record is updated, and sets the modified field accordingly."""
  target.modified = datetime.now(tz.tzlocal())