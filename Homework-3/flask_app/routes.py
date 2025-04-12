# Author: Prof. MM Ghassemi <ghassem3@msu.edu>
import datetime
from http import HTTPStatus

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
    return db.reversibleEncrypt('decrypt', session['email']) if 'email' in session else 'Unknown'


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
    session['email'] = db.reversibleEncrypt('encrypt', form_fields['email'])
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
    # print(db.query('SELECT * FROM users'))
    return render_template('home.html', user=getUser())


@app.route("/static/<path:path>")
def static_dir(path):
    return send_from_directory("static", path)


@app.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    return r

@app.route('/projects')
def projects():
    return render_template('projects.html', user=getUser())


@app.route('/resume')
def resume():
    resume_data = db.getResumeData()
    print(type(resume_data))
    pprint(resume_data)
    return render_template('resume.html', resume_data=resume_data, user=getUser())


@app.route('/processfeedback', methods=['POST'])
def processfeedback():
    feedback = request.form

    # check to make sure the required fields are present
    if 'name' not in feedback or 'email' not in feedback:
        return 'Missing required fields', HTTPStatus.BAD_REQUEST


    db.insertRows('feedback', ['name', 'email', 'comment'], [[feedback['name'], feedback['email'], feedback['comment'] if 'comment' in feedback else 'NULL']])

    feedback = db.query("SELECT name, email, comment FROM feedback")

    return render_template('processfeedback.html', allfeedback=feedback, user=getUser())

@app.route('/piano')
def piano():
    return render_template('piano.html', user=getUser())

#######################################################################################
# TESTING
#######################################################################################
def custom_serializer(obj):
    if isinstance(obj, (datetime.date, datetime.datetime)):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")

# This is a route that will return a jsonified version of whatever table is specified
@app.route('/get/<table>')
def get_table(table):
    data = db.query(f'SELECT * FROM {table}')
    response = app.response_class(
        response=json.dumps(data, default=custom_serializer),
        status=200,
        mimetype='application/json'
    )
    return response