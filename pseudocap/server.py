from flask import Flask, render_template, session, request, Response, jsonify
from api_blueprint import api
from flask.ext import login as login

from functools import wraps
from datetime import timedelta
from loginmgr import login_manager

import models
import base64
import os

app = Flask('pseudo-cap')
app.debug = True
app.secret_key = '\xa85h\x98\x0e\xc34\xa4e\xca\xc6\xb5UX\xb6\xbc\x05\x10;\xa3\xc8\xf1\xa3\xea'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL','sqlite:///database.db')
app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(seconds=15)
app.register_blueprint(api,url_prefix = '/api')

from database import db
db.init_app(app)

class User(login.UserMixin):
  def __init__(self,**kwargs):
      self.name = kwargs['name']
  def get_id(self):
      return self.name
  def name(self):
      return self.name

def check_login(username,password):
    print 'checking {} {}'.format(username,password)
    return (username == 'admin' and password == 'secret')

def check_access_key(username,accesskey):
    print 'accesskey checking {} {}'.format(username,accesskey)
    user = models.User.query.filter_by(name = username).first()
    if not user:
        return None
    
    valid_keys = user.access_keys.all()
    if accesskey in [x.key for x in valid_keys]:
        return user
    else:
        return None

login_manager.init_app(app)
    
@login_manager.user_loader
def load_user(userid):
    return User(name = 'admin') if userid == 'admin' else None

@login_manager.header_loader
def load_user_from_header(header_val):
    header_val = header_val.replace('Basic ', '', 1)
    try:
        header_val = base64.b64decode(header_val)
    except TypeError:
        pass
    
    user,pswd = header_val.split(':',1)
    user =  User(name = user) if check_access_key(user,pswd) else None
    return user
        

@app.route('/')
def home():
    return render_template('home.html')

@app.before_request
def make_session_permanent():
    session.permanent = True 

@app.route('/checkcookie')
@login.login_required
def who():
    
    print session
    print login.current_user
    return jsonify(user = 'bla')
    return jsonify(user = session['user_id'])

@app.route('/logout')
@login.login_required
def logout():
    login.logout_user()
    return ''

@app.route('/getcookie')
def get_cookie():
    auth = request.authorization
    if check_login(auth.username,auth.password):
        print 'login ok!'
        user = User(name = 'admin', authenticated = True)
        login.login_user(user)
        return 'logged in!'
    else:
        print 'login bad!'
        return 'nope', 401


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host = '0.0.0.0', port = port)