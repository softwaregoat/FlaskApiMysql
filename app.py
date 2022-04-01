# Store this code in 'app.py' file
from flask import Flask, json, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import base64

app = Flask(__name__)

f = open('config.json')
data = json.load(f)
f.close()

app.secret_key = data['API_KEY']


app.config['MYSQL_HOST'] = data['MYSQL_HOST']
app.config['MYSQL_USER'] = data['MYSQL_USER']
app.config['MYSQL_PASSWORD'] = data['MYSQL_PASSWORD']
app.config['MYSQL_DB'] = data['MYSQL_DB']


mysql = MySQL(app)


@app.route('/')
def welcome():
    return 'API works'

@app.route('/login', methods =['GET', 'POST'])
def login():
    msg = 'Failed'
    if request.method == 'POST':
        try:
            username = request.args.get('username')
            password = request.args.get('password')
            print(username, password)
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM user WHERE username = % s AND password = % s', (username, password ),)
            user = cursor.fetchone()
            if user:
                session['loggedin'] = True
                session['id'] = user['id']
                session['username'] = user['username']
                msg = 'Logged in successfully !'
            else:
                msg = 'Incorrect username / password !'

        except Exception as ex:
            msg = ex
    return msg, 200

@app.route('/controller-temaplate', methods =['GET', 'POST'])
def get_controller_template():
    msg = 'Failed'
    if session['loggedin'] != True:
        msg = "No logged in session"
        return msg, 400

    user_id = session.get("id")
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM controller_template WHERE user_id = % s', (str(user_id) ),)
    templates = cursor.fetchall()
    if templates:
        json_data=[]
        for result in templates:
            json_data.append(result)
        return json.dumps(json_data), 200
    else:
        msg = 'Incorrect username / password !'

    return msg, 200

# id=?
@app.route('/controller-application', methods =['GET', 'POST'])
def get_controller_application():
    msg = 'Failed'
    if session['loggedin'] != True:
        msg = "No logged in session"
        return msg, 400

    id = request.args.get('id')
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM controller_appllication_param WHERE template_id = % s', (str(id) ),)
    templates = cursor.fetchall()
    if templates:
        json_data=[]
        for result in templates:
            json_data.append(result)
        return json.dumps(json_data), 200
    else:
        msg = 'No Control Application Parameters'

    return msg, 200

# id=?
@app.route('/controller-variable', methods =['GET', 'POST'])
def get_controller_variable():
    msg = 'Failed'
    if session['loggedin'] != True:
        msg = "No logged in session"
        return msg, 400

    id = request.args.get('id')
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM controller_variable_param WHERE template_id = % s', (str(id) ),)
    templates = cursor.fetchall()
    if templates:
        json_data=[]
        for result in templates:
            json_data.append(result)
        return json.dumps(json_data), 200
    else:
        msg = 'No Controlled Variable Parameters'

    return msg, 200

# id=?
@app.route('/disturbance-variable', methods =['GET', 'POST'])
def get_disturbance_variable():
    msg = 'Failed'
    if session['loggedin'] != True:
        msg = "No logged in session"
        return msg, 400

    id = request.args.get('id')
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM disturbance_variable_param WHERE template_id = % s', (str(id) ),)
    templates = cursor.fetchall()
    if templates:
        json_data=[]
        for result in templates:
            json_data.append(result)
        return json.dumps(json_data), 200
    else:
        msg = 'No Disturbance Variable Parameters'

    return msg, 200


@app.route('/manipulated-variable', methods =['GET', 'POST'])
def get_manipulated_variable():
    msg = 'Failed'
    if session['loggedin'] != True:
        msg = "No logged in session"
        return msg, 400

    id = request.args.get('id')
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM manipulated_variable_param WHERE template_id = % s', (str(id) ),)
    templates = cursor.fetchall()
    if templates:
        json_data=[]
        for result in templates:
            json_data.append(result)
        return json.dumps(json_data), 200
    else:
        msg = 'No Manipulated Variable Parameters'

    return msg, 200


# id=?
@app.route('/numerical-mapping', methods =['GET', 'POST'])
def get_numerical_mapping():
    msg = 'Failed'
    if session['loggedin'] != True:
        msg = "No logged in session"
        return msg, 400

    id = request.args.get('id')
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM numerical_mapping WHERE template_id = % s', (str(id) ),)
    templates = cursor.fetchall()
    if templates:
        json_data=[]
        for result in templates:
            json_data.append(result)
        return json.dumps(json_data), 200
    else:
        msg = 'No Numerical Mapping data'

    return msg, 200


# @app.route('/register', methods =['GET', 'POST'])
# def register():
# 	msg = ''
# 	if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form and 'address' in request.form and 'city' in request.form and 'country' in request.form and 'postalcode' in request.form and 'organisation' in request.form:
# 		username = request.form['username']
# 		password = request.form['password']
# 		email = request.form['email']
# 		organisation = request.form['organisation']
# 		address = request.form['address']
# 		city = request.form['city']
# 		state = request.form['state']
# 		country = request.form['country']	
# 		postalcode = request.form['postalcode']
# 		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
# 		cursor.execute('SELECT * FROM accounts WHERE username = % s', (username, ))
# 		account = cursor.fetchone()
# 		if account:
# 			msg = 'Account already exists !'
# 		elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
# 			msg = 'Invalid email address !'
# 		elif not re.match(r'[A-Za-z0-9]+', username):
# 			msg = 'name must contain only characters and numbers !'
# 		else:
# 			cursor.execute('INSERT INTO accounts VALUES (NULL, % s, % s, % s, % s, % s, % s, % s, % s, % s)', (username, password, email, organisation, address, city, state, country, postalcode, ))
# 			mysql.connection.commit()
# 			msg = 'You have successfully registered !'
# 	elif request.method == 'POST':
# 		msg = 'Please fill out the form !'
# 	return render_template('register.html', msg = msg)


# @app.route("/display")
# def display():
# 	if 'loggedin' in session:
# 		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
# 		cursor.execute('SELECT * FROM accounts WHERE id = % s', (session['id'], ))
# 		account = cursor.fetchone()	
# 		return render_template("display.html", account = account)
# 	return redirect(url_for('login'))

# @app.route("/update", methods =['GET', 'POST'])
# def update():
# 	msg = ''
# 	if 'loggedin' in session:
# 		if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form and 'address' in request.form and 'city' in request.form and 'country' in request.form and 'postalcode' in request.form and 'organisation' in request.form:
# 			username = request.form['username']
# 			password = request.form['password']
# 			email = request.form['email']
# 			organisation = request.form['organisation']
# 			address = request.form['address']
# 			city = request.form['city']
# 			state = request.form['state']
# 			country = request.form['country']	
# 			postalcode = request.form['postalcode']
# 			cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
# 			cursor.execute('SELECT * FROM accounts WHERE username = % s', (username, ))
# 			account = cursor.fetchone()
# 			if account:
# 				msg = 'Account already exists !'
# 			elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
# 				msg = 'Invalid email address !'
# 			elif not re.match(r'[A-Za-z0-9]+', username):
# 				msg = 'name must contain only characters and numbers !'
# 			else:
# 				cursor.execute('UPDATE accounts SET username =% s, password =% s, email =% s, organisation =% s, address =% s, city =% s, state =% s, country =% s, postalcode =% s WHERE id =% s', (username, password, email, organisation, address, city, state, country, postalcode, (session['id'], ), ))
# 				mysql.connection.commit()
# 				msg = 'You have successfully updated !'
# 		elif request.method == 'POST':
# 			msg = 'Please fill out the form !'
# 		return render_template("update.html", msg = msg)
# 	return redirect(url_for('login'))

if __name__ == "__main__":
	app.run(host ="localhost", port = int("5000"))
