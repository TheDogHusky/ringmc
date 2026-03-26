from sqlalchemy import Column, Integer, String, event
from sqlalchemy.orm import declarative_base
from datetime import datetime
from dateutil import tz

Base = declarative_base()

# TODO: finir, et faire upload des images (figure it out)
class Build(Base):
    __tablename__ = 'builds'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    images = Column(String) # sera serialized en JSON pour stocker la liste des URLs des images du build
    # Date de publication, automatique
    created = Column(String)
    modified = Column(String)

# https://stackoverflow.com/questions/13978554
@event.listen(Build, 'before_insert')
def update_created_modified_on_create_listener(mapper, connection, target):
  """ Event listener that runs before a record is updated, and sets the create/modified field accordingly."""
  target.created = datetime.utcnow()
  target.modified = datetime.utcnow()

@event.listen(Build, 'before_update')
def update_modified_on_update_listener(mapper, connection, target):
  """ Event listener that runs before a record is updated, and sets the modified field accordingly."""
  target.modified = datetime.now(tz.tzlocal())