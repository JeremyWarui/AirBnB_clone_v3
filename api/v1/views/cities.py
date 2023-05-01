#!/usr/bin/python3
"""cities RESTful API actions"""
from models.city import City
from models.state import State
from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage


@app_views.route("/states/<state_id>/cities",
                 methods=["GET"], strict_slashes=False)
def all_cities(state_id):
    """retrives all cities"""
    states = storage.get(State, state_id)
    city_list = []
    if states is None:
        abort(404)

    for city in states.cities:
        city_list.append(city.to_dict())
    return jsonify(city_list), 200


@app_views.route("cities/<city_id>", methods=["GET"], strict_slashes=False)
def get_city(city_id):
    """retrives city of given id"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    else:
        return jsonify(city.to_dict()), 200


@app_views.route("/cities/<city_id>", methods=["DELETE"], strict_slashes=False)
def del_city(city_id):
    """deletes a city"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    city.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/states/<state_id>/cities",
                 methods=["POST"], strict_slashes=False)
def new_city(state_id):
    """adds a new city"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    elif "name" not in data:
        return jsonify({"error": "Missing name"}), 400
    else:
        data['state_id'] = state_id
        new_city = City(**data)
        new_city.save()
        return jsonify(new_city.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=["PUT"], strict_slashes=False)
def update_city(city_id):
    """update an existing city"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    else:
        data = request.get_json()
        if data is None:
            return jsonify({"error": "Not a JSON"}), 400
        else:
            city.name = data['name']
            city.save()
            return jsonify(city.to_dict()), 200
