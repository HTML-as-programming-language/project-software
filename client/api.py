from flask import Flask, request, jsonify
from moduleview import ModuleView

app = Flask(__name__)

_myapp = None

def set_app(a):
    global _myapp

    _myapp = a

@app.route("/module/<module_id>/add")
def add_module(module_id):
    content = ""
    try:
        content = request.get_json(force=True)
    except:
        pass

    module = ModuleView(content)
    _myapp.add_module(module)

    return jsonify(True)

@app.route("/module/<module_id>/delete")
def delete_module(module_id):
    _myapp.remove_module(module_id)

    return jsonify(True)

