#!/usr/bin/python3
"""cities module"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'])
def get_users():
    '''retrive list of all users'''
    if request.method == 'GET':
        users = list(map(lambda obj: obj.to_dict(),
                         storage.all(User).values()))
        return jsonify(users)


@app_views.route('/users/', methods=['POST'])
def create_users():
    '''creates a new user to acheive the POST method goal'''
    data = request.get_json(silent=True)

    if not data:
        abort(400, description='Not a JSON')
    if 'email' not in data:
        abort(400, description='Missing email')
    if 'password' not in data:
        abort(400, description='Missing password')

    new_user = User(**data)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['GET', 'DELETE', 'PUT'])
def get_user(user_id):
    '''retrive the User matches with the id'''
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    if request.method == 'GET':
        return jsonify(user.to_dict())
    elif request.method == 'DELETE':
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
    else:
        data = request.get_json(silent=True)

        if not data:
            abort(400, description="Not a JSON")
        else:
            for k, v in data.items():
                if k in ['id', 'email', 'created_at', 'updated_at']:
                    continue
                else:
                    setattr(user, k, v)
            user.save()
            return jsonify(user.to_dict()), 200
