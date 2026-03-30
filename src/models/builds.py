from sqlalchemy import Integer, String, event
from sqlalchemy.orm import declarative_base, mapped_column
from datetime import datetime
from dateutil import tz
from ..extensions import db

# TODO: finir, et faire upload des images (figure it out)
class Build(db.Model):
    __tablename__ = 'builds'
    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String)
    description = mapped_column(String)
    images = mapped_column(String) # sera serialized en JSON pour stocker la liste des URLs des images du build
    # Date de publication, automatique
    created = mapped_column(String)
    modified = mapped_column(String)

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