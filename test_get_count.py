#!/usr/bin/python3
""" Test .get() and .count() methods
"""
from models import storage
from models.state import State
from models.city import City
from models.place import Place
from models.user import User
from models.amenity import Amenity
from models.review import Review


print("All objects: {}".format(storage.count()))
print("State objects: {}".format(storage.count(State)))
print("State objects: {}".format(storage.count(City)))
print("State objects: {}".format(storage.count(Place)))
print("State objects: {}".format(storage.count(User)))
print("State objects: {}".format(storage.count(Amenity)))
print("State objects: {}".format(storage.count(Review)))


first_state_id = list(storage.all(State).values())[0].id
print("First state: {}".format(storage.get(State, first_state_id)))
