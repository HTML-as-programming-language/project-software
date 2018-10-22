from flask import Flask, render_template, send_from_directory
app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/<path:path>')
def recourse(path):
    return send_from_directory('templates', path)

if __name__ == '__main__':
    app.run(debug=True, port=5003)