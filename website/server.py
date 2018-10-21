from flask import Flask
app = Flask(__name__)

from flask import render_template, send_from_directory


@app.route('/')
def index():
    return render_template('test2.html')

@app.route('/<path:path>')
def recourse(path):
    return send_from_directory('templates', path)