from flask import Flask, request, jsonify
import datetime
from client import SensorType


class Client:
    def __init__(self, callback):
        self.callback = callback
        self.last_keep_alive = datetime.datetime.now()

clients = {}

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

    if content in clients:
        # TODO
        #return json_err("callback already exists")
        pass

    c = Client(content)
    clients[content] = c

    # TODO: Return current modules.

    return jsonify({
        "modules": [format_module(key, m) for key, m in _b.clients.items()]
    })

@app.route("/keepalive")
def keep_alive():
    content = ""
    try:
        content = request.get_json(force=True)
    except:
        pass

    if not content:
        return json_err("endpoint not given")

    if content not in clients:
        return json_err("given endpoint not known")

    clients[content].last_keep_alive = datetime.datetime.now()
    
    return jsonify(True)

@app.route("/module/<module_id>/setting/<setting_key>", methods=["post"])
def module_setting_set(module_id, setting_key):
    client_maintenance()

    content = ""
    try:
        content = request.get_json(force=True)
    except:
        pass

    if module_id not in _b.clients:
        return json_err("module does not exist")

    if setting_key == "hatch_force":
        if content:
            _b.clients[module_id].open_hatch()
        else:
            _b.clients[module_id].close_hatch()
    else:
        return json_err("unknown setting")

    return jsonify(True)

@app.route("/module/<module_id>/sensor/<sensor_id>/<sensor_setting_key>", methods=["post"])
def module_sensor_setting_set(module_id, sensor_id, sensor_setting_key):
    client_maintenance()

    content = ""
    try:
        content = request.get_json(force=True)
    except:
        pass

    if module_id not in _b.clients:
        return json_err("module does not exist")

    if sensor_setting_key == "temp_threshold":
        if type(content) is not list or len(content) < 2:
            return json_err("not two temps provided for temp")
            
        _b.clients[module_id].set_threshold_open_temperature(int(content[0]))
        _b.clients[module_id].set_threshold_close_temperature(int(content[1]))
    elif sensor_setting_key == "light_threshold":
        if type(content) is not list or len(content) < 2:
            return json_err("not two intensities provided for light")
            
        _b.clients[module_id].set_threshold_open_lightintensity(int(content[0]))
        _b.clients[module_id].set_threshold_close_lightintensity(int(content[1]))
    else:
        return json_err("unknown setting")

    return jsonify(True)

def client_maintenance():
    now = datetime.datetime.now()

    to_rem = []

    for key, c in clients.items():
        diff = now - c.last_keep_alive
        print(diff.seconds)
        if diff.seconds > 15:
            print("Remove inactive client:", c.callback)

            to_rem.append(key)

    for c in to_rem:
        del clients[c]

def format_module(mid, m):
    return {
        "id": mid,
        "label": m.port,
        "data": {
            "labelHatch open": str(m.current_pos) + "%",
            "hatch_status": m.current_pos,
        },
        "sensors": [format_module_sensor(stype, m) for stype in m.supported_sensors],
    }

def format_module_sensor(stype, m):
    data = {}

    if stype is SensorType.TEMP:
        data["id"] = "0"
        data["type"] = "TEMP"
        data["label"] = "Temperature"
        data["data"] = {
            "temp": m.current_temp,
            "label": str(m.current_temp) + "C"
        }
        data["settings"] = []
        data["settings"].append({
            "id": "temp_threshold",
            "label": "Temperature thresholds",
            "type": "int",
            "subtype": "minmax",
            "min": 0,
            "max": 30,
        })
    elif stype is SensorType.LIGHT:
        data["id"] = "1"
        data["type"] = "LIGHT"
        data["label"] = "Light"
        data["data"] = {
            "temp": m.current_light,
            "label": str(m.current_light) + "%"
        }
        data["settings"] = []
        data["settings"].append({
            "id": "temp_threshold",
            "label": "Light thresholds",
            "type": "int",
            "subtype": "minmax",
            "min": 0,
            "max": 100,
        })

    return data

def json_err(msg):
    # TODO: return HTTP error code.
    return '{"error": "' + msg + '"}\n', 400
