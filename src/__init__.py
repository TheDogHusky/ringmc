from flask import Flask, render_template, request, g
from dotenv import load_dotenv
from pathlib import Path
from .extensions import db
import os

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data.db"

    project_root = Path(app.root_path).parent
    builds_upload_folder = project_root / 'src' / 'static' / 'uploads' / 'builds'
    builds_upload_folder.mkdir(parents=True, exist_ok=True)
    app.config['UPLOAD_FOLDER_BUILDS'] = str(builds_upload_folder)

    db.init_app(app)

    @app.before_request
    def lock_down():
        cookie = request.cookies.get('password')
        g.is_admin = (cookie == os.getenv('ADMIN_PASS'))
        g.logged_in = cookie in [os.getenv('ADMIN_PASS'), os.getenv('USER_PASS')]

        if not g.logged_in:
            if request.path.startswith('/static/') or request.path == '/login':
                return None
            return render_template('lockdown.html')
        return None

    @app.context_processor
    def inject_globals():
        return {
            "is_admin": getattr(g, "is_admin", False),
            "logged_in": getattr(g, "logged_in", False),
        }
    
    from .index import index
    from .articles import articles
    from .builds import builds
    
    app.register_blueprint(index)
    app.register_blueprint(articles, url_prefix='/articles')
    app.register_blueprint(builds, url_prefix='/builds')

    return app