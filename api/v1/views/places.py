#!/usr/bin/python3
'''places module'''
from flask import jsonify, request, abort
from . import app_views
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET'])
def get_places_of_city(city_id):
    '''retrives list of all Place objects'''
    my_city = storage.get(City, city_id)
    if not my_city:
        abort(404)

    related_places = list(map(lambda obj: obj.to_dict(), my_city.places))
    return jsonify(related_places)


@app_views.route('/cities/<city_id>/places/', methods=['POST'])
def creates_place_in_city(city_id):
    '''retrives list of all Place objects'''
    my_city = storage.get(City, city_id)
    if not my_city:
        abort(404)

    data = request.get_json(silent=True)

    if not data:
        abort(400, description='Not a JSON')
    if 'user_id' not in data:
        abort(400, description='Missing user_id')

    my_user = storage.get(User, data['user_id'])

    if not my_user:
        abort(404)
    if 'name' not in data:
        abort(400, description='Missing name')

    data['city_id'] = city_id
    new_place = Place(**data)
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['GET', 'DELETE', 'PUT'])
def get_delete_place(place_id):
    '''retrives or deletes specific Place matches with given id'''
    my_place = storage.get(Place, place_id)
    if not my_place:
        abort(404)

    if request.method == 'GET':
        return jsonify(my_place.to_dict())
    elif request.method == 'DELETE':
        storage.delete(my_place)
        storage.save()
        return jsonify({}), 200
    else:
        data = request.get_json(silent=True)
        if not data:
            abort(400, description='Not a JSON')

        for k, v in data.items():
            if k in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
                continue
            else:
                setattr(my_place, k, v)
        my_place.save()
        return jsonify(my_place.to_dict()), 200
