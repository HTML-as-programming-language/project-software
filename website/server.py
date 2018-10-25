from flask import Flask, render_template, send_from_directory, request
import subprocess
app = Flask(__name__)


def compile_screen(screenname):
    subprocess.call('./reactivate.sh', shell=True)
    subprocess.call('./compile.sh ' + screenname, shell=True)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/<path:path>')
def recourse(path):
    return send_from_directory('templates', path)


@app.route('/screen/<path:path>')
def screens(path):
    screenname = path.split(".")[0]
    if request.args.get('compile') == "true":
        compile_screen(screenname)
        
    if "." in path:
        return send_from_directory("templates/screens/"+screenname, path)
    else:
        return render_template("screens/"+path+"/"+path+".html")


@app.route('/compile/<path:screenname>')
def compile(screenname):
    compile_screen(screenname)
    return "oke"


if __name__ == '__main__':
    app.run(debug=True, port=5003)