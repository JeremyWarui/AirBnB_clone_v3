#!/usr/bin/python3
""" index file that serves the static files """
from api.v1.views import app_views
from flask import jsonify


@app_views.route("/status")
def status_route():
    """status route return json status ok"""
    return jsonify({"status": "OK"})
