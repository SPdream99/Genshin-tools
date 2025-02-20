from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_mysqldb import MySQL
import random
import jwt
import string
import datetime
import clientside
import MySQLdb.cursors
import json
class mysql:
    def __init__(self, mysql):
        self.mysql = mysql

    def check_loggedin(self):
        if "loggedin" in session:
            return True
        return False

    def check_cre(self):
        cookie=clientside.get_cookie("cre")
        mysql=self.mysql
        if cookie!=None:
            cookie=jwt.decode(cookie, "1707", algorithms=["HS384"])
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM credentials WHERE id = % s AND username = % s AND credentials = % s', (cookie["id"],cookie["username"], cookie["cre"]))
            account = cursor.fetchone()
            if account:
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
            if 'id' in session and "username" in session:
                cursor.execute("DELETE FROM credentials WHERE id = % s AND username = % s", (session['id'],session['username']))
            mysql.connection.commit()
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
        cursor.execute('INSERT INTO accounts VALUES (NULL, % s, % s, % s,False,NULL,% s)', (username, password, email, datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=datetime.timezone.utc) ))
        mysql.connection.commit()
        account=self.check_account(username)
        if account:
            j=json.dumps({})
            cursor.execute(f'INSERT INTO storage VALUES (% s, % s, "[]", % s)',(account["id"],username,j))
            mysql.connection.commit()

    def get_account(self,username, password):
        mysql=self.mysql
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = % s AND password = % s', (username, password))
        account = cursor.fetchone()
        return account

    def check_verify(self,account):
        account=self.check_account(account)
        now=datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=datetime.timezone.utc)
        date_compare=account["CodeExpire"].replace(tzinfo=datetime.timezone.utc)>now
        return [account["isVerified"],account["email"],date_compare]

    def create_code(self,account):
        mysql=self.mysql
        code=''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(4))
        time=(datetime.datetime.now(datetime.timezone.utc)+datetime.timedelta(seconds=60*10)).replace(tzinfo=datetime.timezone.utc).strftime("%Y/%m/%d %H:%M:%S")
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("UPDATE accounts SET VerifyCode=% s WHERE username=% s", (code, account))
        cursor.execute("UPDATE accounts SET CodeExpire=% s WHERE username=% s", (time, account))
        mysql.connection.commit()
        return code

    def check_code(self,account,code):
        account=self.check_account(account)
        code_compare=(code==account["VerifyCode"])
        if  code_compare !=True:
            return 'Wrong code'
        now=datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=datetime.timezone.utc)
        date_compare=account["CodeExpire"].replace(tzinfo=datetime.timezone.utc)>now
        if date_compare!=True:
            return 'This code is no longer availale'
        return True

    def verify(self,account):
        mysql=self.mysql
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("UPDATE accounts SET isVerified=% s WHERE username=% s", (True, account))
        cursor.execute("UPDATE accounts SET VerifyCode=% s WHERE username=% s", (None, account))
        cursor.execute("UPDATE accounts SET CodeExpire=% s WHERE username=% s", (None, account))
        mysql.connection.commit()
        return True

    def get_star_character(self,account):
        mysql=self.mysql
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM storage WHERE username = % s', ([account]))
        account = cursor.fetchone()
        return account

    def set_star_character(self,account,char):
        mysql=self.mysql
        list=self.get_star_character(account)
        account=self.check_account(account)
        if list:
            if list["star_character"]!=None:
                c_list=json.loads(list["star_character"])
            else:
                c_list=[]
            if not char in c_list:
                c_list.append(char)
                a="check"
            else:
                c_list.remove(char)
                a="uncheck"
            c_list=json.dumps(c_list)
            cursor = mysql.connection.cursor()
            cursor.execute("UPDATE storage SET star_character=% s WHERE id=% s", (c_list, account["id"]))
            mysql.connection.commit()
            return [True,a]
        return [False]

    def get_mats(self,account):
        mysql=self.mysql
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM storage WHERE username = % s', ([account]))
        account = cursor.fetchone()
        return account

    def set_mats(self,account,mat,quantity):
        mysql=self.mysql
        list=self.get_mats(account)
        account=self.check_account(account)
        if list and quantity>=0:
            if list["items"]!=None:
                c_list=json.loads(list["items"])
            else:
                c_list={}
            if quantity==0:
                c_list.pop(mat)
            else:
                c_list.update({mat: quantity})
            c_list=json.dumps(c_list)
            cursor = mysql.connection.cursor()
            cursor.execute("UPDATE storage SET items=% s WHERE id=% s", (c_list, account["id"]))
            mysql.connection.commit()
            return True
        return False
