from flask import Blueprint

builds = Blueprint('builds', __name__)

from . import routes