#!/usr/bin/python3
"""states RESTful API actions"""
from models.state import State
from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def get_states():
    """ route that lists all states """
    states = storage.all(State)
    s_list = [state.to_dict() for state in states.values()]
    return jsonify(s_list)


@app_views.route("/states/<state_id>", methods=["GET"], strict_slashes=False)
def get_state(state_id):
    """retrive specific state"""
    states = storage.all(State)
    s_list = [state.to_dict() for state in states.values()]

    for state in s_list:
        if state_id == state['id']:
            return jsonify(state)
        else:
            abort(404)


@app_views.route("/states/<state_id>", methods=["DELETE"], strict_slashes=False)
def del_state(state_id):
    """delete state of specific id"""
    states = storage.all(State)
    s_list = [state.to_dict() for state in states.values()]

    for state in s_list:
        if state_id == state['id']:
            state.delete()
            storage.save()
            return jsonify({}), 200
        else:
            abort(404)


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def new_state():
    """adds new state"""
    state = request.get_json()
    if not state:
        return jsonify({"error": "not valid JSON"}), 400
    elif "name" not in state:
        return jsonify({"error": "Missing name"}), 400
    else:
        new_state = State(**state)
        new_state.save()
        return jsonify(new_state.to_dict()), 201


@app_views.route("/states/<state_id>", methods=["PUT"], strict_slashes=False)
def update_state(state_id):
    """updates state"""
    state = request.get_json()
    if not state:
        return jsonify({"error": "NOt a JSON"}), 400
