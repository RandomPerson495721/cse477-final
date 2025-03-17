# Author: Prof. MM Ghassemi <ghassem3@msu.edu>
from http import HTTPStatus

from flask import current_app as app, jsonify
from flask import render_template, redirect, request
from .utils.database.database import database
from werkzeug.datastructures import ImmutableMultiDict
from pprint import pprint
import json
import random

db = database()


@app.route('/')
def root():
    return redirect('/home')


@app.route('/home')
def home():
    x = random.choice(
        ['I started university when I was a wee lad of 15 years.', 'I have a pet sparrow.', 'I write poetry.'])
    return render_template('home.html', fun_fact=x)


@app.route('/projects')
def projects():
    return render_template('projects.html')


@app.route('/resume')
def resume():
    resume_data = db.getResumeData()
    print(type(resume_data))
    pprint(resume_data)
    return render_template('resume.html', resume_data=resume_data)


@app.route('/processfeedback', methods=['POST'])
def processfeedback():
    feedback = request.form

    # check to make sure the required fields are present
    if 'name' not in feedback or 'email' not in feedback:
        return 'Missing required fields', HTTPStatus.BAD_REQUEST


    db.insertRows('feedback', ['name', 'email', 'comment'], [[feedback['name'], feedback['email'], feedback['comment'] if 'comment' in feedback else 'NULL']])

    feedback = db.query("SELECT name, email, comment FROM feedback")

    return render_template('processfeedback.html', allfeedback=feedback)