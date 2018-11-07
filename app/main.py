from flask import Flask
app = Flask(__name__)

from flask import render_template, send_from_directory


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/<path:path>')
def recourse(path):
    return send_from_directory('templates', path)


if __name__ == '__main__':
    app.run(debug=True, port=8081)