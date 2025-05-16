#!/usr/bin/python3
'''0-hello_route Module'''
from flask import Flask, render_template
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.user import User
from models import storage
from uuid import uuid4


app = Flask(__name__)


@app.route("/states_list", strict_slashes=False)
def states_list():
    '''display the every state and
    the linked cities from DB'''
    states = storage.all(State).values()
    sorted_states = sorted(states, key=lambda state: state.name)
    return render_template('7-states_list.html', states=sorted_states)


@app.route("/cities_by_states", strict_slashes=False)
def cities_by_states():
    '''displays states and everyone
    with it linked cities after'''
    states = storage.all(State).values()
    sorted_states = sorted(states, key=lambda state: state.name)
    return render_template('8-cities_by_states.html', states=sorted_states)


@app.route("/1-hbnb/", strict_slashes=False)
def hbnb():
    '''displayes states, citites, amenities and places objects'''
    states = storage.all(State).values()
    cities = storage.all(City).values()
    amenities = storage.all(Amenity).values()
    places = storage.all(Place).values()
    users = storage.all(User).values()
    return render_template('1-hbnb.html',
                           data={'states': states,
                                 'cities': cities,
                                 'amenities': amenities,
                                 'places': places,
                                 'users': users}, cache_id=uuid4())


@app.teardown_appcontext
def close_session(exception=None):
    '''close session when app context is torn down'''
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
