#!/usr/bin/python3
""" main app file """
import os
from flask import Flask
from models import storage
from api.v1.views import app_views


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(self):
    """ tear down db session """
    storage.close()


if __name__ == "__main__":
    """ listen to specific ports """
    host = os.environ.get("$HBNB_API_HOST", "0.0.0.0")
    port = int(os.environ.get("HBNB_API_PORT", 5000))
    app.run(host=host, port=port, threaded=True)
