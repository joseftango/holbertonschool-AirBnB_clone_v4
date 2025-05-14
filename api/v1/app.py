#!/usr/bin/python3
''' main file of our api application '''
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from flask_cors import CORS
from os import getenv


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown(execption):
    """close the storage instance"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    if getenv('HBNB_API_HOST'):
        Host = getenv('HBNB_API_HOST')
    else:
        Host = '0.0.0.0'
    if getenv('HBNB_API_PORT'):
        Port = getenv('HBNB_API_PORT')
    else:
        Port = 5000

    app.run(host=Host, port=Port, threaded=True)
