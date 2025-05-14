#!/usr/bin/python3
'''places_reviews module'''
from flask import jsonify, abort, request
from . import app_views
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from models.review import Review


@app_views.route('/places/<place_id>/reviews')
def place_reviews(place_id):
    '''Retrieves the list of all Review objects of a Place'''
    my_place = storage.get(Place, place_id)
    if not my_place:
        abort(404)
    linked_reviews = list(map(lambda obj: obj.to_dict(), my_place.reviews))
    return jsonify(linked_reviews)


@app_views.route('/places/<place_id>/reviews/', methods=['POST'])
def creates_review_of_place(place_id):
    '''creates a new Review object of Place'''
    my_place = storage.get(Place, place_id)
    data = request.get_json(silent=True)
    if not my_place:
        abort(404)
    if not data:
        abort(400, description='Not a JSON')
    if 'user_id' not in data:
        abort(400, description='Missing user_id')
    if not storage.get(User, data['user_id']):
        abort(404)
    if 'text' not in data:
        abort(400, description='Missing text')

    data['place_id'] = place_id
    new_review = Review(**data)
    new_review.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['GET', 'DELETE', 'PUT'])
def get_review(review_id):
    '''retrives Review object based on review_id'''
    my_review = storage.get(Review, review_id)
    if not my_review:
        abort(404)
    if request.method == 'GET':
        return jsonify(my_review.to_dict())
    elif request.method == 'DELETE':
        storage.delete(my_review)
        storage.save()
        return jsonify({}), 200
    else:
        data = request.get_json(silent=True)
        if not data:
            abort(400, 'Not a JSON')
        for k, v in data.items():
            if k in ['id', 'user_id', 'place_id', 'created_at', 'updated_at']:
                continue
            else:
                setattr(my_review, k, v)
        my_review.save()
        return jsonify(my_review.to_dict()), 200
