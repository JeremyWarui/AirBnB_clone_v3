#!/usr/bin/python3
"""rest api for users"""
from flask import request, abort, jsonify
from models.user import User
from models import storage
from api.v1.views import app_views


@app_views.route("/users", methods=["GET"], strict_slashes=False)
def get_users():
    """retrive all users"""
    users = storage.all(User)
    users_list = [user.to_dict() for user in users.values()]
    return jsonify(users_list), 200


@app_views.route("/users/<user_id>", methods=["GET"], strict_slashes=False)
def get_user(user_id):
    """get specific user"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict()), 200


@app_views.route("/users/<user_id>", methods=["DELETE"], strict_slashes=False)
def del_user(user_id):
    """delete specific user"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    user.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def new_user():
    """add a new user"""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    if "email" not in data.keys():
        return jsonify({"error": "Missing email"}), 400
    if "password" not in data:
        return jsonify({"error": "Missing password"}), 400
    user = User(**data)
    storage.new(user)
    storage.save()
    return jsonify(user.to_dict()), 201


@app_views.route("/users/<user_id>", methods=["PUT"], strict_slashes=False)
def update_user(user_id):
    """update specific user"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    for key, val in data.items():
        if key not in ["id", "email", "created_at", "updated_at"]:
            setattr(user, key, val)
    storage.save()
    return jsonify(user.to_dict()), 200
