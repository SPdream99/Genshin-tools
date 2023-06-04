from flask import Flask, render_template, request, redirect, url_for, session, abort, make_response

def write_cookie(id,var,ex,template):
    resp = make_response(redirect(template))
    resp.set_cookie(id,var, max_age=ex)
    return resp

def get_cookie(id):
    return request.cookies[id]