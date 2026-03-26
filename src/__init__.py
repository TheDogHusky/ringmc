import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{app.root_path}/data.db"

    db = SQLAlchemy(app) # todo finir et mettre les autres arguments -> base declarative et tout

    from .index import index as index_blueprint
    from .articles import articles as articles_blueprint
    
    app.register_blueprint(index_blueprint)
    app.register_blueprint(articles_blueprint, url_prefix='/articles')

    return app