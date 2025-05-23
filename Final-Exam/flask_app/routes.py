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
    return redirect('/home')


@app.route('/processlogin', methods=["POST", "GET"])
def processlogin():
    form_fields = dict((key, request.form.getlist(key)[0]) for key in list(request.form.keys()))

    # Check if the email and password are correct
    user = db.getUser(form_fields['email'])

    if len(user) == 0 or db.authenticate(form_fields['email'], form_fields['password'])['success'] == 0:
        session['login_attempt'] = session.get('login_attempt', 0) + 1
        return json.dumps(
            {'success': 0, 'error': 'Incorrect email or password', 'login_attempt': session['login_attempt']})

    session['login_attempt'] = 0
    session['email'] = db.reversibleEncrypt('encrypt', form_fields['email'])
    return json.dumps({'success': 1})


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/processregister', methods=["POST", "GET"])
def processregister():
    # Check if the email and password are correct
    return db.createUser(request.form['email'], request.form['password'], 'guest')

@app.route('/createevent')
@login_required
def createevent():
    return render_template('createevent.html', user=getUser())


@app.route('/processcreateevent', methods=["POST", "GET"])
@login_required
def processcreateevent():
    # Event Name: a short descriptive title for the event (e.g., “Team Meeting Scheduler”).
    # Start Date and End Date: these define the date range over which availability will be collected. Both dates must be inclusive.
    # Daily Time Range: the hours of the day in which availability will be collected (e.g., 8:00 AM to 8:00 PM).
    # List of Invitee Emails: a comma-separated list of email addresses belonging to registered users who should be allowed to view and participate in the event.

    # Get the form data
    form_fields = dict((key, request.form.getlist(key)[0]) for key in list(request.form.keys()))

    event_id = db.createEvent(user=db.getUser(getUser())['user_id'], name=form_fields['event_name'], start_date=form_fields['start_date'],
                   end_date=form_fields['end_date'], start_time=form_fields['start_time'],
                   end_time=form_fields['end_time'], invitee_emails=form_fields['invitee_emails'])
    # Check if the event was created successfully
    if event_id["success"] == 1:
        return redirect('/event/' + str(event_id["event_id"]))
    else:
        return json.dumps({'success': 0, 'error': 'Event creation failed'})


@app.route('/joinevent')
@login_required
def joinevent():
    return render_template('joinevent.html', user=getUser(), events=db.getUserEvents(user=db.getUser(getUser())))


@app.route('/processjoinevent', methods=["POST", "GET"])
@login_required
def processjoinevent():
    return json.dumps({'success': 0})


@app.route('/event/<event_id>')
@login_required
def event(event_id):
    # Check if the event exists
    _event = db.getEvent(event_id)
    if len(_event) == 0:
        return redirect('/home')

    # Check to see if user is an invitee
    if getUser() not in _event['invitee_emails'] and _event['owner_id'] != db.getUser(getUser())['user_id']:
        return 'You don\'t have permission to access this page', HTTPStatus.FORBIDDEN

    session['event_id'] = event_id

    return render_template('event.html', event=_event, user=getUser(), slots=db.getUserAvailability(event_id=event_id, user=db.getUser(getUser())['user_id']), timedelta=datetime.timedelta, datetime=datetime)


@app.route('/event/<event_id>/getavailability')
@login_required
def get_availability(event_id):
    # Check if the event exists
    _event = db.getEvent(event_id)
    if len(_event) == 0:
        return redirect('/home')

    # Check to see if user is logged in
    if 'email' not in session:
        return redirect('/login')

    # # Check to see if user is an invitee
    # if getUser() not in _event['invitee_emails']:
    #     return 'You don\'t have permission to access this page', HTTPStatus.FORBIDDEN

    # Get the availability data
    availability = db.getUserAvailability(db.getUser(getUser())['user_id'], event_id)
    # content type = application/json
    return json.dumps(availability), {'Content-Type': 'application/json'}



#########################################################################################
# SOCKETIO RELATED
#########################################################################################

@socketio.on('connect', namespace='/availability')
def connect():
    event_id = session.get('event_id')
    # Join the room for the event
    if event_id:
        join_room(event_id)
        print(f'Client joined room {event_id}')

@socketio.on('disconnect', namespace='/availability')
def disconnect():
    event_id = session.get('event_id')
    # Leave the room for the event
    if event_id:
        leave_room(event_id)
        print(f'Client left room {event_id}')

    session['event_id'] = None


@socketio.on('update_availability', namespace='/availability')
def update_availability(data):
    print(data)
    event_id = data['event_id']
    data = data['slot_states']
    db.updateUserAvailability(event_id=event_id, user=db.getUser(getUser())['user_id'], slots=data)


    data = db.getHeatmapData(event_id)
    socketio.emit('update_heatmap', {'event_id': event_id, 'slot_states': json.dumps(data)}, namespace='/availability')


@socketio.on('get_heatmap', namespace='/availability')
def get_heatmap(event_id):
    # Check if the event exists
    _event = db.getEvent(event_id)
    # Get the availability data
    availability = db.getHeatmapData(event_id)
    # content type = application/json
    return json.dumps(availability), {'Content-Type': 'application/json'}


#######################################################################################
# OTHER
#######################################################################################
@app.route('/')
def root():
    return redirect('/home')


@app.route('/home')
@login_required
def home():
    return render_template('event_portal.html', user=getUser())


@app.route("/static/<path:path>")
def static_dir(path):
    return send_from_directory("static", path)


@app.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    return r

#######################################################################################
# TESTING
#######################################################################################
# def custom_serializer(obj):
#     if isinstance(obj, (datetime.date, datetime.datetime)):
#         return obj.isoformat()
#     raise TypeError(f"Type {type(obj)} not serializable")


# # This is a route that will return a jsonified version of whatever table is specified
# @app.route('/get/<table>')
# def get_table(table):
#     data = db.query(f'SELECT * FROM {table}')
#     response = app.response_class(response=json.dumps(data, default=custom_serializer), status=200,
#         mimetype='application/json')
#     return response
