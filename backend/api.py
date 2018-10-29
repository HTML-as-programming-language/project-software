from flask import Flask, request, jsonify
import datetime


class Client:
    def __init__(self, callback):
        self.callback = callback
        self.last_keep_alive = datetime.datetime.now()

clients = []

app = Flask(__name__)

_b = None

def set_backend(b):
    global _b
    _b = b

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

    if not content:
        return json_err("no callback given")

    c = Client(content)
    clients.append(c)

    # TODO: Return current modules.

    return jsonify({
        "modules": [format_module(m) for m in _b.clients]
    })

@app.route("/module/<module_id>", methods=["post"])
def st00fs(module_id):
    print(module_id)
    return ""

@app.route("/module/<module_id>/setting/<setting_key>", methods=["post"])
def module_setting_set(module_id, setting_key):
    content = ""
    try:
        content = request.get_json(force=True)
    except:
        pass

    if module_id not in _b.clients:
        return json_err("module does not exist")

    if setting_key == "hatch_force":
        if content == "true":
            _b.clients[module_id].open_hatch()
        else:
            _b.clients[module_id].close_hatch()
    else:
        return json_err("unknown setting")

    return jsonify(True)

@app.route("/module/<module_id>/sensor/<sensor_id>/<sensor_setting_key>", methods=["post"])
def module_sensor_setting_set(module_id, sensor_id, sensor_setting_key):
    content = ""
    try:
        content = request.get_json(force=True)
    except:
        pass

    if module_id not in _b.clients:
        return json_err("module does not exist")

    if setting_key == "temp_threshold":
        if type(content) is not list or len(content) < 2:
            return json_err("not two temps provided for temp")
            
        _b.clients[module_id].set_threshold_open_temperature(int(content[0]))
        _b.clients[module_id].set_threshold_close_temperature(int(content[1]))
    elif setting_key == "light_threshold":
        if type(content) is not list or len(content) < 2:
            return json_err("not two intensities provided for light")
            
        _b.clients[module_id].set_threshold_open_lightintensity(int(content[0]))
        _b.clients[module_id].set_threshold_close_lightintensity(int(content[1]))
    else:
        return json_err("unknown setting")

    return jsonify(True)

def format_module(m):
    return {
        "id": m.port,
        "label": m.port,
        "data": {
            "hatch_status": m.current_pos,
        },
        "sensors": [format_module_sensor(s)],
    }

def format_module_sensor(m):
    return {}

def json_err(msg):
    return '{"error": "' + msg + '"}\n'
