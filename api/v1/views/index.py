#!/usr/bin/python3
""" index file that serves the static files """
from api.v1.views import app_views
from flask import jsonify
from models.state import State
from models.place import Place
from models.city import City
from models.amenity import Amenity
from models.review import Review
from models.user import User
from models import storage


@app_views.route("/status", methods=["GET"], strict_slashes=False)
def status_route():
    """status route return json status ok"""
    return jsonify({"status": "OK"})


@app_views.route("/stats", methods=["GET"], strict_slashes=False)
def stats():
    """return count of each objects by type"""
    count_dict = {}
    count_dict["amenities"] = storage.count(Amenity)
    count_dict["cities"] = storage.count(City)
    count_dict["places"] = storage.count(Place)
    count_dict["reviews"] = storage.count(Review)
    count_dict["states"] = storage.count(State)
    count_dict["users"] = storage.count(User)
    return jsonify(count_dict)
