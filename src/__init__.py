from flask import Flask
from .extensions import db

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data.db"

    db.init_app(app)
    
    from .index import index
    from .articles import articles
    
    app.register_blueprint(index)
    app.register_blueprint(articles, url_prefix='/articles')

    return app