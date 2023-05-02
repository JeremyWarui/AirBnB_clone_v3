#!/usr/bin/python3
"""rest api for places"""
from flask import request, abort, jsonify
from models.place import Place
from models.city import City
from models.user import User
from models import storage
from api.v1.views import app_views


@app_views.route("/cities/<city_id>/places", methods=["GET"],
                 strict_slashes=False)
def get_places(city_id):
    """retrive all places"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    place_list = [place.to_dict() for place in city.places]
    return jsonify(place_list), 200


@app_views.route("/places/<place_id>", methods=["GET"], strict_slashes=False)
def get_place(place_id):
    """retrive on place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict()), 200


@app_views.route("/places/<place_id>", methods=["DELETE"],
                 strict_slashes=False)
def del_place(place_id):
    """delete place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    place.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/cities/<city_id>/places", methods=["POST"],
                 strict_slashes=False)
def new_place(city_id):
    """add new place"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    data = request.get_json()
    if not data:
        return jsonify({"error": "NOt a JSON"})
    if "user_id" not in data:
        return jsonify({"error": "Missing user_id"})
    if not storage.get(User, data["user_id"]):
        abort(404)
    if "name" not in data:
        return jsonify({"error": "Missing name"})
    place = Place(**data)
    place["city_id"] = city_id
    storage.new(place)
    storage.save()
    return jsonify(place.to_dict()), 201


@app_views.route("/places/<place_id>", methods=["PUT"], strict_slashes=False)
def update_place(place_id):
    """update existing place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    for key, val in data.keys():
        if key not in ["id", "user_id", "city_id", "created_at",
                       "updated_at"]:
            setattr(place, key, val)
    storage.save()
    return jsonify(place.to_dict()), 200
