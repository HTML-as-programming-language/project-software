from server import app

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Sneeuwpop'}
    return '''
<html>
    <head>
        <title>Home Page - Microblog</title>
    </head>
    <body>
        <h1>Hello, ''' + user['username'] + '''!</h1>
    </body>
</html>'''

# @app.route("/")
# @app.route("/index")
# def index():
#     return render_template('index.html', title='Home')

# @app.route("/login")
# def module_id():
#     return render_template('login.html', title='Login')

# @app.route("/dashboard")
# def module():
#     return render_template('dashboard.html', title='Dashboard')


# if __name__ == '__main__':
#     app.run(debug=True, port=8080)