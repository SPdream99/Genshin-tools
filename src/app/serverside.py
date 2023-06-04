from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import random
import string
import MySQLdb.cursors
import re

def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)

def check_loggedin():
    try:
        logged_in=session['loggedin']
    except:
        logged_in=None
    return logged_in

def make_credentials():
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(70))
    return result_str
