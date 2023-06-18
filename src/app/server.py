from flask import Flask, render_template, request, redirect, url_for, session, abort
from flask_mysqldb import MySQL
import sys
import MySQLdb.cursors
import re
import serverside as ss
import clientside as cs
import genshinAPI as gAPI
import wikiaAPI as wAPI

app = Flask(__name__)
app.secret_key = 'Itsnew'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123'
app.config['MYSQL_DB'] = 'login'
mysql = MySQL(app)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('Errors/404.html'), 404

@app.errorhandler(404)
def server_error(e):
    return render_template('Errors/500.html'), 500

@app.route('/')
def index():
    msg=''
    if ss.check_loggedin():
        return render_template('index.html', msg = msg)
    else:
        return redirect(url_for('login'))

@app.route('/login', methods =['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = % s AND password = % s', (username, password, ))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            msg = 'Logged in successfully !'
            cre=ss.make_credentials()
            return cs.write_cookie("cre",cre,60*60*24*399,url_for("index"))
        else:
            msg = 'Incorrect username / password !'
    if ss.check_loggedin():
        return redirect(url_for("index"))
    else:
        return render_template('login.html', msg = msg)

@app.route('/logout')
def logout():
    ss.logout()
    return redirect(request.referrer)

@app.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form :
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = % s', (username, ))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password or not email:
            msg = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO accounts VALUES (NULL, % s, % s, % s)', (username, password, email, ))
            mysql.connection.commit()
            msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    if ss.check_loggedin():
        return redirect(url_for("index"))
    else:
        return render_template('register.html', msg = msg)

@app.route('/characters/<char>/star/<check>', methods =['GET', 'POST'])
def character_star(star,check):
    return render_template(url_for("character_list.html"))

@app.route('/characters/<char>', methods =['GET', 'POST'])
def character(char):
    list=gAPI.get_character_list()
    if char in list:
        return render_template("character.html",name=char)
    else:
        abort(404)

@app.route('/characters', methods =['GET', 'POST'])
def CharactersList():
    c_list=[]
    ic_list={}
    e_list=[]
    c_list=gAPI.get_character_list()
    ic_list=gAPI.get_character()
    e_list=gAPI.get_element_list()
    return render_template("character_list.html",list=c_list,ic_list=ic_list,e_list=e_list)

@app.route('/weapons', methods =['GET', 'POST'])
def WeaponsList():
    w_list=[]
    w_list=gAPI.get_weapon_list()
    return render_template("weapon_list.html",list=w_list)