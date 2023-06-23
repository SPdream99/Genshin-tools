from flask import Flask, render_template, request, redirect, url_for, session, abort, jsonify
from flask_mysqldb import MySQL
from flask_mailing import Mail, Message
import sys
import MySQLdb.cursors
import re
import serverside
import clientside as cs
import genshinAPI as gAPI
import os

def c_print(c):
    print(c, file=sys.stderr)

if os.environ.get("email") and os.environ.get("password"):
    mail_os=True
else:
    mail_os=False

app = Flask(__name__)
app.secret_key = 'Itsnew'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123'
app.config['MYSQL_DB'] = 'data'
if mail_os:
    app.config['MAIL_SERVER']='smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USERNAME'] = os.environ.get("email")
    app.config['MAIL_PASSWORD'] = os.environ.get("password")
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False
    app.config['TESTING'] = False
    mail = Mail(app)
mysql = MySQL(app)
ss=serverside.mysql(mysql)

@app.before_request
def check_login():
    if ss.check_loggedin():
        return
    checked=ss.check_cre()
    if checked[0]:
        session['loggedin'] = True
        session['id'] = checked[1]
        session['username'] = checked[2]
        return
    if cs.get_cookie("cre")!=None:
        return cs.logout(request.referrer)
    return

@app.errorhandler(404)
def page_not_found(e):
    return render_template('Errors/404.html'), 404

@app.errorhandler(500)
def internal_error(e):
    return render_template('Errors/500.html'), 500

@app.route('/send_email')
async def mailing():
    if mail_os:
        message = Message(
            subject="Flask-Mailing module test html mail",
            recipients=["anhnguyennhat878@gmail.com"],
            body="This is the basic email body"
            )
        await mail.send_message(message)
        return jsonify(status_code=200, content={"message": "email has been sent"})
    else:
        return ""

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
        account=ss.get_account(username, password)
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            msg = 'Logged in successfully !'
            if(request.form.get('remember')=="remembered"):
                ss.remove_cre()
                cre=ss.make_credentials(account['id'],account['username'])
                return cs.write_cookie("cre",cre,60*60*24*399,url_for("index"))
        else:
            msg = 'Incorrect username / password !'
    if ss.check_loggedin():
        return redirect(url_for("index"))
    else:
        return render_template('login.html', msg = msg)

@app.route('/logout')
def logout():
    ss.remove_cre()
    return cs.logout(request.referrer)

@app.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form :
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        account=ss.check_account(username)
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password or not email:
            msg = 'Please fill out the form !'
        else:
            ss.add_account(username, password, email )
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
        return render_template("character.html",char=gAPI.get_character(char))
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