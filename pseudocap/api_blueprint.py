from flask import Blueprint, jsonify
import json
from loginmgr import login_manager
from flask.ext import login

api = Blueprint('api', __name__)

@api.route('/workflow/<name>')
@login.login_required
def workflow(name):
    data = json.load(open('capdata/{}/workflow.json'.format(name)))
    return jsonify(data = data)

@api.route('/step/<name>/<stepname>')
@login.login_required
def step(name,stepname):
    data = json.load(open('capdata/{}/{}_step_spec.json'.format(name,stepname)))
    return jsonify(data = data)

@api.route('/node/<name>/<stepname>')
@login.login_required
def node(name,stepname):
    data = json.load(open('capdata/{}/{}_node_spec.json'.format(name,stepname)))
    return jsonify(data = data)

    
    