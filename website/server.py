from flask import Flask, render_template, send_from_directory, request
import subprocess
app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/<path:path>')
def recourse(path):
    return send_from_directory('templates', path)


@app.route('/screen/<path:path>')
def screens(path):
    if request.args.get("compile") == "true":
        compile(path)

    if "." in path:
        return send_from_directory("templates/screens/"+path.split(".")[0], path)
    else:
        return render_template("screens/"+path+"/"+path+".html")


if __name__ == '__main__':
    app.run(debug=True, port=5003)


def compile(path):
    subprocess.call(['./compile.sh'])