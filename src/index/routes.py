from flask import request, render_template
from . import index

from ..models.articles import Article

from ..extensions import db

@index.route('/', methods=['GET', 'POST'])
def index():
    articles = db.session.execute(db.select(Article)).scalars().all()
    return render_template('index.html', articles=articles)