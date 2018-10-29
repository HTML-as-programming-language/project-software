from flask import Flask, request
import datetime

app = Flask(__name__)

class Client:
    def __init__(self, callback):
        self.callback = callback
        self.last_keep_alive = datetime.datetime.now()


clients = []

@app.route("/")
def hello():
    return "HTML-as-programming-language / project-software / backend"

@app.route("/init", methods=["post"])
def init():
    content = ""
    try:
        content = request.get_json(force=True)
    except:
        pass

    # TODO: Check if callback has been given.
    if not content:
        return json_err("no callback given")

    c = Client(content)

    # TODO: Return current modules.
    print(content)

    return "{}\n"


def json_err(msg):
    return '{"error": "' + msg + '"}\n'
