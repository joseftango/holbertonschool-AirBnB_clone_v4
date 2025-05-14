#!/usr/bin/python3
"""cities module"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities')
def all_amenities():
    '''Retrieves the list of all Amenity objects'''
    amenities = list(map(lambda obj: obj.to_dict(),
                         storage.all(Amenity).values()))
    return jsonify(amenities)


@app_views.route('/amenities/', methods=['POST'])
def creates_amenity():
    '''creates a new Amenity object in storage'''
    data = request.get_json(silent=True)
    if not data:
        abort(400, description='Not a JSON')
    elif 'name' not in data:
        abort(400, description='Missing name')
    else:
        new_amenity = Amenity(**data)
        new_amenity.save()
        return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['GET', 'DELETE', 'PUT'])
def get_amenity(amenity_id):
    '''Retrieves a Amenity object based on it id'''
    my_amenity = storage.get(Amenity, amenity_id)
    if not my_amenity:
        abort(404)
    if request.method == 'GET':
        return jsonify(my_amenity.to_dict())
    elif request.method == 'DELETE':
        storage.delete(my_amenity)
        storage.save()
        return jsonify({}), 200
    else:
        data = request.get_json(silent=True)
        if not data:
            abort(400, description='Not a JSON')
        else:
            for k, v in data.items():
                if k in ['id', 'created_at', 'updated_at']:
                    continue
                else:
                    setattr(my_amenity, k, v)
                my_amenity.save()
            return jsonify(my_amenity.to_dict()), 200
