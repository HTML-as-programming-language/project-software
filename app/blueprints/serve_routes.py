from flask import render_template, send_from_directory
from flask import Blueprint

serve_routes = Blueprint('serve_routes', __name__)


@serve_routes.route('/')
@serve_routes.route('/index')
def index():
    return render_template('index.html')


@serve_routes.route('/<path:path>')
def recourse(path):
    return send_from_directory('templates', path)

