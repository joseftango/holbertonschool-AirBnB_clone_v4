#!/usr/bin/python3
"""cities module"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'])
def state_related_cities(state_id):
    '''Retrieves the list of all City objects of
    specific State or creates a city'''
    my_state = storage.get(State, state_id)
    if not my_state:
        abort(404)
    related_cities = list(map(lambda obj: obj.to_dict(), my_state.cities))
    return jsonify(related_cities)


@app_views.route('/states/<state_id>/cities/', methods=['POST'])
def new_city_in_state(state_id):
    '''creates a new City related to a specific State'''
    my_state = storage.get(State, state_id)

    if not my_state:
        abort(404)

    data = request.get_json(silent=True)

    if data is None:
        return abort(400, "Not a JSON")
    if "name" not in data:
        return abort(400, "Missing name")
    else:
        data['state_id'] = my_state.id
        my_city = City(**data)
        my_city.save()
        return jsonify(my_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['GET', 'DELETE', 'PUT'])
def city_obj(city_id):
    '''Retrieves a City object based on city_id'''
    my_city = storage.get(City, city_id)
    if not my_city:
        abort(404)
    if request.method == 'GET':
        return jsonify(my_city.to_dict())
    elif request.method == 'DELETE':
        storage.delete(my_city)
        storage.save()
        return jsonify({}), 200
    else:
        data = request.get_json(silent=True)
        if data:
            for k, v in data.items():
                if k in ['id', 'state_id', 'created_at', 'updated_at']:
                    continue
                else:
                    setattr(my_city, k, v)
            my_city.save()
            return jsonify(my_city.to_dict()), 200
        else:
            abort(400, description='Not a JSON')
