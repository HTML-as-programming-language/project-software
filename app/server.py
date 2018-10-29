from flask import Flask, render_template, send_from_directory
app = Flask(__name__)


from jinja2 import Environment
from hamlish_jinja import HamlishExtension

env = Environment(extensions=[HamlishExtension])


@app.route("/")
@app.route("/index")
def index():
    return render_template('index.html', title='Home')

@app.route("/login")
def module_id():
    return render_template('login.html', title='Login')

@app.route("/dashboard")
def module():
    return render_template('dashboard.html', title='Dashboard')


if __name__ == '__main__':
    app.run(debug=True, port=8080)
