from flask import Flask, render_template, request, redirect, url_for, session, abort, jsonify, flash
from flask_mysqldb import MySQL
from flask_mailing import Mail, Message
import sys
import MySQLdb.cursors
import re
import serverside
import clientside as cs
import genshinAPI as gAPI
import wikiaAPI as wiki
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
    checked=ss.check_cre()
    if cs.get_cookie("cre")!=None:
        if checked[0]==False:
            return cs.remove_cookie('cre',request.referrer)
    if ss.check_loggedin():
        account=ss.check_account(session['username'])
        if account:
            check=ss.check_verify(session["username"])
            if not check[0]:
                session["isVerified"]=check[0]
                return
            else:
                session["isVerified"]=check[0]
                return
        else:
            session.clear()
    if checked[0]:
        session['loggedin'] = True
        session['id'] = checked[1]
        session['username'] = checked[2]
        check=ss.check_verify(session["username"])
        if not check[0]:
            session["isVerified"]=check[0]
        else:
            session["isVerified"]=check[0]
        return
    return

@app.errorhandler(404)
def page_not_found(e):
    return render_template('Errors/404.html'), 404

@app.errorhandler(500)
def internal_error(e):
    return render_template('Errors/500.html'), 500

@app.route('/')
def index():
    return render_template('index.html')

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
        if msg!="":
            flash(msg)
        return render_template('login.html')

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
            account=ss.get_account(username, password)
            if account:
                session['loggedin'] = True
                session['id'] = account['id']
                session['username'] = account['username']
                return redirect(url_for("send_code"))
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    if ss.check_loggedin():
        return redirect(url_for("index"))
    else:
        if msg!="":
            flash(msg)
        return render_template('register.html')

@app.route('/verify', methods =['GET', 'POST'])
def mail_verify():
    msg=''
    if request.method == 'POST' and 'code' in request.form:
        if ss.check_loggedin():
            check=ss.check_verify(session["username"])
            if not check[0]:
                result=ss.check_code(session["username"],request.form['code'])
                if result!=True:
                    msg=result
                    if msg!="":
                        flash(msg)
                    return render_template("verify_mail.html",msg=msg,user=session["username"],mail=check[1],onCooldown=check[2])
                else:
                    if ss.verify(session["username"]):
                        flash("Your email have been verified")
                        return redirect(url_for("index"))
            abort(500)
    if ss.check_loggedin():
        check=ss.check_verify(session["username"])
        if not check[0]:
            if msg!="":
                flash(msg)
            return render_template("verify_mail.html",user=session["username"],mail=check[1],onCooldown=check[2])
        else:
            return redirect(url_for("index"))
    else:
        return redirect(url_for("login"))

@app.route('/characters/star/<check>', methods =['GET', 'POST'])
def character_star(check):
    if ss.check_loggedin():
        if session["isVerified"]:
            if request.method == 'POST' and "id" in request.json and check=="check":
                set=ss.set_star_character(session["username"], request.json["id"])
                if set[0]:
                    return jsonify(status_code=200, content={"message": f"character {set[1]}"})
            if check=="list":
                list=ss.get_star_character(session["username"])
                if list:
                    return jsonify(status_code=200, content={"char":list["star_character"]})
        else:
            flash("Please verify your account")
            return jsonify(status_code=400, content="Please verify your account")
    else:
        flash("Please log in")
        return jsonify(status_code=400, content="Please log in")
    return abort(500)

@app.route('/characters/<char>', methods =['GET', 'POST'])
def character(char):
    list=gAPI.get_character_list()
    if char in list:
        char_info=gAPI.get_character(char)
        img_list=char_info.img_list
        return render_template("character.html",char=char_info,img=img_list)
    else:
        abort(404)

@app.route('/characters', methods =['GET', 'POST'])
def CharactersList():
    c_list=[]
    ic_list={}
    e_list=[]
    s_list=[]
    c_list=gAPI.get_character_list()
    ic_list=gAPI.get_character()
    e_list=gAPI.get_element_list()
    if ss.check_loggedin:
        if "username" in session:
            if session["isVerified"]:
                get=ss.get_star_character(session["username"])
                if get:
                    s_list=get["star_character"]
    return render_template("character_list.html",list=c_list,ic_list=ic_list,e_list=e_list,s_list=s_list)

@app.route('/weapons', methods =['GET', 'POST'])
def WeaponsList():
    w_list=[]
    w_list=gAPI.get_weapon_list()
    return render_template("weapon_list.html",list=w_list)

@app.route('/verify_sendcode')
async def send_code():
    if mail_os:
        if ss.check_loggedin():
            check=ss.check_verify(session["username"])
            if not check[0]:
                if not check[2]:
                    email=check[1]
                    code=ss.create_code(session["username"])
                    name=session["username"]
                    message = Message(
                        subject="Verification code",
                        recipients=[email],
                        html=render_template('Mails/template.html',code=code,name=name,link=request.url_root[0:-1]+url_for("mail_verify"))
                        )
                    await mail.send_message(message)
                    flash("Verification code sent")
                    return redirect(url_for("mail_verify"))
                else:
                    return abort(500)
            else:
                return abort(500)
        else:
            return abort(500)
    else:
        return abort(500)
