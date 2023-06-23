from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_mysqldb import MySQL
from flask_mailing import Mail, Message
import random
import jwt
import string
import datetime
import clientside
import MySQLdb.cursors
class mysql:
    def __init__(self, mysql):
        self.mysql = mysql

    def check_loggedin(self):
        try:
            logged_in=session['loggedin']
        except:
            logged_in=False
        return logged_in

    def check_cre(self):
        cookie=clientside.get_cookie("cre")
        mysql=self.mysql
        if cookie!=None:
            cookie=jwt.decode(cookie, "1707", algorithms=["HS384"])
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM credentials WHERE id = % s AND username = % s AND credentials = % s', (cookie["id"],cookie["username"], cookie["cre"]))
            account = cursor.fetchone()
            now=datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=datetime.timezone.utc)
            date_compare=account["expire"].replace(tzinfo=datetime.timezone.utc)>now
            if not date_compare:
                self.remove_cre([cookie["id"],cookie["username"]])
            if account!=None and date_compare:
                return [True,account["id"],account["username"]]
        return [False]

    def remove_cre(self,u=None):
        mysql=self.mysql
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        if u==None:
            cursor.execute("DELETE FROM credentials WHERE id = % s AND username = % s", (session['id'],session['username']))
        else:
            cursor.execute("DELETE FROM credentials WHERE id = % s AND username = % s", (u[0],u[1]))
        mysql.connection.commit()

    def make_credentials(self,id,u):
        mysql=self.mysql
        letters = string.ascii_lowercase
        result_str = ''.join(random.choice(letters) for i in range(70))
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO credentials VALUES (% s, % s, % s, % s)', (id,u,result_str, (datetime.datetime.now(datetime.timezone.utc)+datetime.timedelta(seconds=60*60*24*399)).replace(tzinfo=datetime.timezone.utc).strftime("%Y/%m/%d %H:%M:%S")))
        mysql.connection.commit()
        return jwt.encode({"username":u,"id":id,"cre":result_str}, "1707", algorithm="HS384")

    def check_account(self,username):
        mysql=self.mysql
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = % s', ([username]))
        account = cursor.fetchone()
        return account

    def add_account(self,username,password,email):
        mysql=self.mysql
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO accounts VALUES (NULL, % s, % s, % s)', (username, password, email ))
        mysql.connection.commit()

    def get_account(self,username, password):
        mysql=self.mysql
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = % s AND password = % s', (username, password))
        account = cursor.fetchone()
        return account
