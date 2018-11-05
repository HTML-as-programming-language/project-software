from flask import Flask, render_template, send_from_directory
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

from routes import *

if __name__ == '__main__':
    app.run(debug=True, port=8080)