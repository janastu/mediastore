#!/usr/bin/env python
#-*- coding: utf-8 -*-

from flask import (Flask, request, session, g, redirect, url_for, abort, render_template, 
        jsonify, Response, send_from_directory)
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_oauthlib.client import OAuth
import yaml
import os
import datetime
import soundfile as sf
import io
import pydub
from functools import wraps

def check_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        access_token = session.get('access_token')
        if access_token is None:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

app = Flask(__name__)
app.config.from_object(__name__)
if os.path.exists("mediastore/config.yaml"):
    with open("mediastore/config.yaml") as f:
        app.config.update(yaml.load(f))

app.config.from_envvar('MEDIASTORE_CONFIG', silent=True)

if app.config.get("SECRET_KEY") is None:
    app.config['SECRET_KEY'] = os.urandom(24)

CORS(app)
oauth = OAuth(app)

github = oauth.remote_app(
        'github',
        app_key='GITHUB',
	request_token_params={'scope': ''},
	base_url='https://api.github.com/',
	request_token_url=None,
	access_token_method='POST',
	access_token_url='https://github.com/login/oauth/access_token',
	authorize_url='https://github.com/login/oauth/authorize'
)

#directory where main.py is run from the parent directory of this file
MAIN_DIR = os.path.abspath(os.path.join(app.root_path, os.pardir))

@app.route("/")
def index():
    access_token = session.get('access_token')
    if access_token is not None:
        info = github.get("user")
    else:
        info = ""

    return render_template("index.html", **locals())

@app.route("/api/media", methods=['POST'])
@check_auth
def create_media():
    data = request.data
    filename = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S.mp3")
    user = github.get("user")
    userdir = os.path.join(app.config['UPLOAD_FOLDER'], user.data['login'])

    #wavdata, samplerate = sf.read(io.BytesIO(data))
    if not os.path.exists(userdir):
        os.makedirs(userdir)
    #sf.write(os.path.join(userdir, filename), wavdata, samplerate)
    audio = pydub.AudioSegment(io.BytesIO(data))
    audio.export(os.path.join(userdir, filename))

    return jsonify({ 
        "response": "success",
        "uri": "{}/media/{}/{}".format(request.base_url, user.data['login'], filename)
        })

# will be hooked up to serve directly from nginx
# this is for the development version
@app.route("/media/<path:path>")
def serve_media(path):
    #return send_from_directory(app.config['UPLOAD_FOLDER'], path)
    upload_dir = app.config['UPLOAD_FOLDER']
    if not upload_dir.startswith("/"): #if it is not an absolute path then figure out the relative path
        upload_dir = os.path.join(MAIN_DIR, upload_dir)
    return send_from_directory(upload_dir, path)

@app.route("/me")
def get_me():
    me = github.get("user")
    return jsonify(me.data)

@app.route("/login")
def login():
    return github.authorize(callback=url_for('authorized', _external=True))

@app.route("/authorized")
def authorized():
    resp = github.authorized_response()
    error = ""
    error_description = ""
    if resp is None or resp.get("access_token") is None:
        error = request.args['error']
        error_description = request.args['error_description']
        user = None
    else:
        session['access_token'] = (resp['access_token'], '')
        user = github.get('user').data

    return render_template("authorized.html", user=user, error=error, error_description=error_description)

@github.tokengetter
def github_auth_token():
    return session.get("access_token")
