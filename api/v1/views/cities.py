#!/usr/bin/python3
"""cities RESTful API actions"""
from models.city import City
from models.state import State
from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage


@app_views.route("/states/<state_id>/cities", methods=["GET"], strict_slashes=False)
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
    return jsonify(city.to_dict()), 200


@app_views.route("/cities/<city_id>", methods=["DELETE"], strict_slashes=False)
def del_city(city_id):
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    city.delete()
    storage.save()
    return jsonify({}), 200
