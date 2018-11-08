from flask import Flask
from app.blueprints import serve_routes, serve_sockets

app = Flask(__name__)
app.register_blueprint(serve_routes)
app.register_blueprint(serve_sockets)

if __name__ == '__main__':
    app.run(debug=True, port=8081)