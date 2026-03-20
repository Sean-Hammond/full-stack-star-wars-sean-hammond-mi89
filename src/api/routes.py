"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User, Character, Planet, Favorite_Character, Favorite_Planet
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from sqlalchemy import select

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)


@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }

    return jsonify(response_body), 200

@api.route("/people", methods=["GET"])
def get_all_people():
    all_people = db.session.execute(select(Character)).scalars().all()
    people_dictionaries = []
    for person in all_people:
        people_dictionaries.append(person.serialize())
    return jsonify(people_dictionaries), 200

@api.route("/people/<int:people_id>", methods=["GET"])
def get_single_person(people_id):
    single_person = db.session.get(Character, people_id)  # Recommended direct method
    if single_person is None:
        return jsonify({"message": "character not found"}), 404
    return jsonify(single_person.serialize()), 200

@api.route("/planets", methods=["GET"])
def get_planets():
    pass

@api.route("/planets/<int:planet_id>", methods=["GET"])
def get_single_planet(planet_id):
    pass

@api.route("/user", methods=["GET"])
def get_users():
    pass

@api.route("/users/<int:user_id>/favorites", methods=["GET"])
def get_favorites(user_id):
    pass

# We will send the user in the body 
@api.route("/favorite/planet/<int:planet_id>", methods=["POST"])
def add_favorite_planet(planet_id):
    pass

@api.route("/favorite/people/<int:people_id>", methods=["POST"])
def add_favorite_person(people_id):
    pass

@api.route("/favorite/planet/<int:planet_id>", methods=["DELETE"])
def delete_favorite_planet(planet_id):
    pass

@api.route("/favorite/people/<int:people_id>", methods=["DELETE"])
def delete_favorite_person(people_id):
    pass