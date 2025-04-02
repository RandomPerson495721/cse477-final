# Author: Prof. MM Ghassemi <ghassem3@msu.edu>
from flask import current_app as app, send_from_directory
from flask import render_template, redirect, request, session, url_for, copy_current_request_context
from flask_socketio import SocketIO, emit, join_room, leave_room, close_room, rooms, disconnect
from .utils.database.database import database
from werkzeug.datastructures import ImmutableMultiDict
from pprint import pprint
import json
import random
import functools
from . import socketio

db = database()


#######################################################################################
# AUTHENTICATION RELATED
#######################################################################################
def login_required(func):
    @functools.wraps(func)
    def secure_function(*args, **kwargs):
        if "email" not in session:
            return redirect(url_for("login", next=request.url))
        return func(*args, **kwargs)

    return secure_function


def getUser():
    return session['email'] if 'email' in session else 'Unknown'


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('email', default=None)
    return redirect('/')


@app.route('/processlogin', methods=["POST", "GET"])
def processlogin():
    form_fields = dict((key, request.form.getlist(key)[0]) for key in list(request.form.keys()))
    session['email'] = form_fields['email']
    return json.dumps({'success': 1})


#######################################################################################
# CHATROOM RELATED
#######################################################################################
@app.route('/chat')
@login_required
def chat():
    return render_template('chat.html', user=getUser())


@socketio.on('joined', namespace='/chat')
def joined(message):
    join_room('main')
    emit('status', {'msg': getUser() + ' has entered the room.', 'style': 'width: 100%;color:blue;text-align: right'},
         room='main')


#######################################################################################
# OTHER
#######################################################################################
@app.route('/')
def root():
    return redirect('/home')


@app.route('/home')
def home():
    print(db.query('SELECT * FROM users'))
    x = random.choice(
        ['I started university when I was a wee lad of 15 years.', 'I have a pet sparrow.', 'I write poetry.'])
    return render_template('home.html', user=getUser(), fun_fact=x)


@app.route("/static/<path:path>")
def static_dir(path):
    return send_from_directory("static", path)


@app.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    return r
