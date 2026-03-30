from flask import request, render_template
from . import articles
from ..models.articles import Article
from ..extensions import db

@articles.route('/', methods=['GET', 'POST'])
def articles_index():
    if request.method == 'POST':
        json_form = request.get_json()
        title = json_form.get('title') if json_form else request.form.get('title')
        content = json_form.get('content') if json_form else request.form.get('content')
        prices = json_form.get('prices') if json_form else None
        image_url = json_form.get('image_url') if json_form else request.form.get('image_url')
        category = json_form.get('category') if json_form else request.form.get('category')
        author = json_form.get('author') if json_form else request.form.get('author')

        # TODO: Add validation for title, content, and prices
        if not title or not content or not prices or not author:
            return "All fields are required", 400

        article = Article(title=title, content=content, prices=prices, image_url=image_url, category=category, author=author)
        db.session.add(article)
        db.session.commit()

    articles = db.session.execute(db.select(Article)).scalars().all()
    return render_template('articles/index.html', articles=articles)

@articles.route('/<int:article_id>')
def article_detail(article_id):
    article = db.session.get(Article, article_id)
    if not article:
        return "Article not found", 404
    return render_template('articles/detail.html', article=article)