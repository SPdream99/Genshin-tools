from flask import Flask, render_template, request, redirect, url_for, session, abort, make_response

def write_cookie(id,var,ex,template):
    resp = make_response(redirect(template))
    resp.set_cookie(id,var, max_age=ex)
    return resp

def remove_cookie(id,template):
    resp = make_response(redirect(template))
    resp.set_cookie(id, '', expires=0)
    return resp

def get_cookie(id):
    if id in request.cookies:
        return request.cookies[id]
    else:
        return None

def logout(template):
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return remove_cookie('cre',template)