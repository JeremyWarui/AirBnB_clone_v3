#!/usr/bin/python3
""" main app file """
import os
from flask import Flask, make_response, jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views


app = Flask(__name__)
CORS(app, resources="/*", origins=["0.0.0.0"])
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(self):
    """ tear down db session """
    storage.close()


@app.errorhandler(404)
def error_404(error):
    """return 404 status code"""
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    """ listen to specific ports """
    host = os.environ.get("HBNB_API_HOST", "0.0.0.0")
    port = int(os.environ.get("HBNB_API_PORT", 5000))
    app.run(host=host, port=port, threaded=True)
