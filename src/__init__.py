import os
from flask import Flask

def create_app():
    app = Flask(__name__)

    from .index import index as index_blueprint
    from .articles import articles as articles_blueprint
    
    app.register_blueprint(index_blueprint)
    app.register_blueprint(articles_blueprint, url_prefix='/articles')

    return app