from flask import request, render_template
from . import index

@index.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')