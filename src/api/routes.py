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
    # (see https://4geeks.com/syllabus/miami-89/read/everything-you-need-to-start-using-sqlalchemy)
    single_person = db.session.get(Character, people_id)
    if single_person is None:
        return jsonify({"message": "character not found"}), 404
    return jsonify(single_person.serialize()), 200


@api.route("/planets", methods=["GET"])
def get_planets():
    all_planets = db.session.execute(select(Planet)).scalars().all()
    planets_dictionaries = []
    for planet in all_planets:
        planets_dictionaries.append(planet.serialize())
    return jsonify(planets_dictionaries), 200


@api.route("/planets/<int:planet_id>", methods=["GET"])
def get_single_planet(planet_id):
    single_planet = db.session.get(Planet, planet_id)
    if single_planet is None:
        return jsonify({"message": "planet not found"}), 404
    return jsonify(single_planet.serialize()), 200


@api.route("/users", methods=["GET"])
def get_users():
    all_users = db.session.execute(select(User)).scalars().all()
    user_dictionaries = []
    for user in all_users:
        user_dictionaries.append(user.serialize())
    return jsonify(user_dictionaries), 200


@api.route("/users/<int:user_id>/favorites", methods=["GET"])
def get_favorites(user_id):
    user = db.session.get(User, user_id)
    if user is None:
        return jsonify({"message": "favorites not found"}), 404
    return jsonify(user.serialize()), 200

# We will send the user in the body


@api.route("/favorite/planet/<int:planet_id>", methods=["POST"])
def add_favorite_planet(planet_id):
    body = request.json
    user = db.session.get(User, body["user_id"])
    planet = db.session.get(Planet, planet_id)
    if user is None or planet is None:
        return jsonify({"message": "invalid user id or favorite planet id"}), 404
    user.favorite_planets.append(planet)
    db.session.commit()
    seralized_user = user.serialize()
    return jsonify(seralized_user["favorite_planets"]), 201


@api.route("/favorite/people/<int:people_id>", methods=["POST"])
def add_favorite_person(people_id):
    body = request.json
    user = db.session.get(User, body["user_id"])
    character = db.session.get(Character, people_id)
    if user is None or character is None:
        return jsonify({"message": "invalid user id or favorite people id"}), 404
    user.favorite_characters.append(character)
    db.session.commit()
    seralized_user = user.serialize()
    return jsonify(seralized_user["favorite_characters"]), 201


@api.route("/favorite/people/<int:people_id>", methods=["DELETE"])
def delete_favorite_person(people_id):
    body = request.json
    user = db.session.get(User, body["user_id"])
    character = db.session.get(Character, people_id)
    if user is None or character is None:
        return jsonify({"message": "invalid user id or favorite people id"}), 404
    user.favorite_characters.remove(character)
    db.session.commit()
    seralized_user = user.serialize()
    return jsonify(seralized_user["favorite_characters"]), 201


@api.route("/favorite/planet/<int:planet_id>", methods=["DELETE"])
def delete_favorite_planet(planet_id):
    body = request.json
    user = db.session.get(User, body["user_id"])
    planet = db.session.get(Planet, planet_id)
    if user is None or planet is None:
        return jsonify({"message": "invalid user id or favorite planet id"}), 404
    user.favorite_planets.remove(planet)
    db.session.commit()
    seralized_user = user.serialize()
    return jsonify(seralized_user["favorite_planets"]), 201


# Update the database by running the terminal commands:
    # $ pipenv run migrate
    # $ pipenv run upgrade
    # $ pipenv run start
