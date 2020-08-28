from flask import Flask, render_template, request, session
from DBcm import UseDatabase

app = Flask(__name__)

app.config['database'] = {'host': '127.0.0.1',
                          'user': 'root',
                          'password': 'kriscoin1234',
                          'database': 'defytheflow_web'}

app.config['current_user'] = {}

def add_user_to_database() -> None:

    with UseDatabase(app.config['database']) as cursor:
        query = """INSERT INTO users (first_name, last_name, login, password)
                   VALUES (%s, %s, %s, %s) """
        cursor.execute(query, (request.form['first_name'].title(), request.form['last_name'].title(),
                               request.form['login'], request.form['password']) )
        app.config['current_user'] = {'first_name': request.form['first_name'],
                                      'last_name' : request.form['last_name'],
                                      'login': request.form['login'],
                                      'password' : request.form['password']}

@app.route('/')
@app.route('/landing.html')
def landing_page() -> 'html':
    try:
        return render_template('logged_in_landing.html', login=app.config['current_user']['login'])
    except:
        return render_template('landing.html')

@app.route('/sign_up.html', methods=['GET', 'POST'])
def sign_up() -> 'html':
    if request.method == 'GET':
        return render_template('sign_up.html')
    else:
        if request.form['password'] != request.form['password_repeat']:
            return render_template('password_fail_sign_up.html')
        else:
            with UseDatabase(app.config['database']) as cursor:
                query = """SELECT * FROM users WHERE login='{}'""".format(request.form['login'])
                cursor.execute(query)
                response = cursor.fetchall()
                if len(response) != 0:
                    return render_template('login_fail_sign_up.html', login=request.form['login'])
                else:
                    add_user_to_database()
                    return render_template('successful_sign_up.html', login=app.config['current_user']['login'])

@app.route('/sign_out.html', methods=['GET'])
def sign_out() -> 'html':
    login = app.config['current_user']['login'][:]
    app.config['current_user'] = {}
    return render_template('sign_out.html', login=login)

@app.route('/log_in.html', methods=['GET', 'POST'])
def log_in() -> 'html':
    if request.method == 'GET':
        return render_template('log_in.html')
    else:
        with UseDatabase(app.config['database']) as cursor:
            query = """SELECT login, password FROM users
                     WHERE login = '{}' and password = '{}'""".format(request.form['login'], request.form['password'])
            cursor.execute(query)
            response = cursor.fetchall()
            if len(response) == 0:
                return render_template('fail_log_in.html')
            else:
                with UseDatabase(app.config['database']) as cursor:
                    query = """SELECT first_name, last_name, login, password FROM users
                             WHERE login = '{}' and password = '{}'""".format(request.form['login'], request.form['password'])
                    cursor.execute(query)
                    response = cursor.fetchall()
                    app.config['current_user']['first_name'] = response[0][0]
                    app.config['current_user']['last_name'] = response[0][1]
                    app.config['current_user']['login'] = response[0][2]
                    app.config['current_user']['password'] = response[0][3]

                return render_template('successful_log_in.html', login=app.config['current_user']['login'],
                                       first_name=app.config['current_user']['first_name'],
                                       last_name=app.config['current_user']['last_name'],
                                       password=app.config['current_user']['password'])

@app.route('/logged_in_landing.html', methods=['GET'])
def logged_in_landing() -> 'html':
    return render_template('logged_in_landing.html', login=app.config['current_user']['login'])

@app.route('/user_profile.html', methods=['GET'])
def user_profile() -> 'html':
    with UseDatabase(app.config['database']) as cursor:
        query = """SELECT first_name, last_name, login, password FROM users
                   WHERE login = '{}'""".format(app.config['current_user']['login'])
        cursor.execute(query)
        response = cursor.fetchall()
        first_name = response[0][0]
        last_name = response[0][1]
        login = response[0][2]
        password = response[0][3]
    return render_template('user_profile.html', login=login,
                                                first_name=first_name,
                                                last_name=last_name,
                                                password=password)

@app.route('/settings.html', methods = ['GET', 'POST'])
def settings() -> 'html':
    if request.method == 'GET':
        return render_template('settings.html', login=app.config['current_user']['login'])
    else:
        with UseDatabase(app.config['database']) as cursor:
            query = """DELETE FROM users WHERE login='{}'""".format(app.config['current_user']['login'])
            cursor.execute(query)
            login = app.config['current_user']['login'][:]
            app.config['current_user'] = {}
            return render_template('account_deleted.html', login=login)

@app.route('/library_app.html', methods=['GET', 'POST'])
def library_app() -> 'html':
    if request.method == 'GET':
        return render_template('library_app.html', login=app.config['current_user']['login'])
    else:
        with UseDatabase(app.config['database']) as cursor:
            query = """SELECT Title, Author, Type, Year, Status
                       FROM books WHERE Title='{}'""".format(request.form['book_title'])
            cursor.execute(query)
            response = cursor.fetchall()
            if len(response) == 0:
                return render_template('library_app.html', title='Unfortunately', author='There is no book',
                                       genre='With the title', year=request.form['book_title'].title(), status='In your library :(')
            else:
                return render_template('library_app.html', title=response[0][0], author=response[0][1],
                                       genre=response[0][2], year=response[0][3], status=response[0][4])




@app.route('/dictionary_app.html', methods=['GET', 'POST'])
def dictionary_app() -> 'html':
    if request.method == 'GET':
        return render_template('dictionary_app.html', login=app.config['current_user']['login'])

if __name__ == '__main__':
    app.run(debug=True)

