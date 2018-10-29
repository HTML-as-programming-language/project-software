from flask import Flask, jsonify
app = Flask(__name__)

from flask import render_template, send_from_directory


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


# @app.route('/get_current_user')
# def get_current_user():
#     return jsonify(username=g.user.username,
#                    email=g.user.email,
#                    id=g.user.id)

if __name__ == '__main__':
    app.run(debug=True, port=8080)
