#!/usr/bin/python3
"""rest api for places"""
from flask import request, abort, jsonify
from models.place import Place
from models.city import City
from models import storage
from api.v1.views import app_views


@app_views.route("/cities/<city_id>/places", methods=["GET"], strict_slashes=False)
def get_places(city_id):
	"""retrive all places"""
	city = storage.get(City, city_id)
	if city is None:
		abort(404)
	place_list = [place.to_dict() for place in city.places]
	return jsonify(place_list), 200


@app_views.route("/places/<place_id>", methods=["GET"], strict_slashes=False)
def get_place(user_id):
	"""retrive on place"""
	place = storage.get(Place, place_id)
	if not place:
		abort(404)
	return jsonify(place.to_dict()), 200


@app_views.route("/places/<place_id>", methods=["DELETE"], strict_slashes=False)
def del_place(place_id):
	"""delete place"""
	place = storage.get(Place, place_id)
	if not place:
		abort(404)
	place.delete()
	storage.save()
	return jsonify({}), 200


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def new_user():


@app_views.route("/users/<user_id>", methods=["PUT"], strict_slashes=False)
def update_user(user_id):
	return jsonify(user.to_dict()), 200
