#!/usr/bin/python3
"""amenities REST api"""
from models.amenity import Amenity
from flask import jsonify, abort, request
from models import storage
from api.v1.views import app_views


@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def get_amenities():
	"""retrive all amenities"""
	amenities = storage.all(Amenity)
	list_amenities = [obj.to_dict() for obj in amenities.values()]
	return jsonify(list_amenities), 200


@app_views.route("/amenities/<amenity_id>", methods=["GET"], strict_slashes=False)
def get_amenity(amenity_id):
	"""get specific amenity given the id"""
	amenity = storage.get(Amenity, amenity_id)
	if amenity is None:
		abort(404)
	return jsonify(amenity.to_dict()), 200


@app_views.route("/amenities/<amenity_id>", methods=["DELETE"],
		strict_slashes=False)
def del_amenity(amenity_id):
	"""delete specific amenity"""
	amenity = storage.get(Amenity, amenity_id)
	if amenity is None:
		abort(404)
	amenity.delete()
	storage.save()
	return jsonify({}), 200


@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def add_amenity():
	"""add a new entry to amenity"""
	data = request.get_json()
	if data is None:
		return jsonify({"error": "Not a JSON"}), 400
	if "name" not in data:
		return jsonify({"error": "Missing name"}), 400
	new_amenity = Amenity(**data)
	storage.new(new_amenity)
	storage.save()
	return jsonify(new_amenity.to_dict()), 201


@app_views.route("/amenities/<amenity_id>", methods=["PUT"],
		strict_slashes=False)
def edit_amenity(amenity_id):
	"""update the amenity"""
	amenity = storage.get(Amenity, amenity_id)
	if amenity is None:
		abort(404)
	data = request.get_json()
	if data is None:
		return jsonify({"error": "Not a JSON"}), 400
	else:
		amenity.name = data["name"]
		storage.save()
		return jsonify({amenity.to_dict()), 200
