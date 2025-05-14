#!/usr/bin/python3
"""index module"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.state import State
from models.city import City
from models.place import Place
from models.review import Review
from models.user import User
from models.amenity import Amenity


@app_views.route('/status')
def status():
    return jsonify({'status': 'OK'})


@app_views.route('/stats')
def stats():
    num_of_states = storage.count(State)
    num_of_cities = storage.count(City)
    num_of_amenities = storage.count(Amenity)
    num_of_places = storage.count(Place)
    num_of_reviews = storage.count(Review)
    num_of_users = storage.count(User)

    statistics = {'amenities': num_of_amenities,
                  'cities': num_of_cities,
                  'places': num_of_places,
                  'reviews': num_of_reviews,
                  'states': num_of_states,
                  'users': num_of_users}

    return jsonify(statistics)
