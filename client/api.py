from flask import Flask, request, jsonify
from moduleview import ModuleView

app = Flask(__name__)

_myapp = None


def set_app(a):
    global _myapp

    _myapp = a


@app.route("/module/<module_id>/add", methods=["post", "get"])
def add_module(module_id):
    content = ""
    try:
        content = request.get_json(force=True)
    except Exception:
        pass

    module = ModuleView(content)
    _myapp.add_module(module)

    return jsonify(True)


@app.route("/module/<module_id>/delete", methods=["post", "get"])
def delete_module(module_id):
    _myapp.remove_module(module_id)

    return jsonify(True)


@app.route("/module/<module_id>/sensor/<sensor_id>/dataitem/<key>",
           methods=["post", "get"])
def change_module_sensor_dataitem(module_id, sensor_id, key):
    content = ""
    try:
        content = request.get_json(force=True)
    except Exception:
        pass

    _myapp.change_module_sensor_dataitem(module_id, sensor_id, key, content)

    return jsonify(True)


@app.route("/module/<module_id>/dataitem/<key>", methods=["post", "get"])
def change_module_dataitem(module_id, key):
    content = ""
    try:
        content = request.get_json(force=True)
    except Exception:
        pass

    _myapp.change_module_dataitem(module_id, key, content)

    return jsonify(True)
