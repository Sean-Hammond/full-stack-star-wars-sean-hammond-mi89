"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User, Character, Planet, Favorite_Character, Favorite_Planet
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from sqlalchemy import select
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)


@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }

    return jsonify(response_body), 200

# The route that creates our token
@api.route("/token", methods=["POST"])
def create_token():
    body = request.json
    user = User.query.filter_by(email-body["email"], password-body["password"]).first()

    if User is None:
        return jsonify(["msg": "Bad email or password"]), 401
    access_token = create_access_token(identity = str(user.id))
    return jsonify({ "token": access_token, "user_id": user.id }), 200


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


@api.route("/favorite/people/<int:people_id>", methods=["POST"])
@jwt_required()
def add_favorite_person(people_id):
    current_user_id = get_jwt_identity()
    if current_user_id is None:
        return jsonify({"message": "invalid or missing user id."}), 400
    user = db.session.get(User, current_user_id)
    character = db.session.get(Character, people_id)
    if user is None or character is None:
        return jsonify({"message": "invalid user id or favorite people id"}), 404

    # OLD CODE to add favorite to database, DIDN'T WORK:
        # user.favorite_characters.append(character)

    # NEW CODE to add favorite to database, NOW TESTING:
    favorite_character = Favorite_Character(
        user_id=user.id, character_id=character.id)
    db.session.add(favorite_character)

    db.session.commit()
    seralized_user = user.serialize()
    # return jsonify(seralized_user["favorite_characters"]), 201
    return jsonify(seralized_user), 201


@api.route("/favorite/planet/<int:planet_id>", methods=["POST"])
def add_favorite_planet(planet_id):
    body = request.json
    if body is None or "user_id" not in body:
        return jsonify({"message": "Please enter a user_id into the body."}), 400
    user = db.session.get(User, body["user_id"])
    planet = db.session.get(Planet, planet_id)
    if user is None or planet is None:
        return jsonify({"message": "invalid user id or favorite planet id"}), 404

    # user.favorite_planets.append(planet)

    favorite_planet = Favorite_Planet(user_id=user.id, planet_id=planet.id)
    db.session.add(favorite_planet)

    db.session.commit()
    seralized_user = user.serialize()
    # return jsonify(seralized_user["favorite_planets"]), 201
    return jsonify(seralized_user), 201


@api.route("/favorite/people/<int:people_id>", methods=["DELETE"])
def delete_favorite_person(people_id):
    body = request.json
    if body is None or "user_id" not in body:
        return jsonify({"message": "Please enter a user_id into the body."}), 400
    user = db.session.get(User, body["user_id"])

    if user is None:
        return jsonify({"message": "invalid user id"}), 404

    # This code finds a record in the Favorite_Character table where the user id in the table matches the user id placed in the body of the request, and where the people id in the url matches a character id in the table, and returns the Favorite_Character object if it exists, or None if not. The scalar part is what either returns the object or none.
    favorite_character = db.session.execute(
        select(Favorite_Character).where(
            (Favorite_Character.user_id == body["user_id"]) &
            (Favorite_Character.character_id == people_id)
        )
    ).scalar_one_or_none()

    if favorite_character is None:
        return jsonify({"message": "that character id is not in this user's favorites"}), 404
    db.session.delete(favorite_character)
    db.session.commit()
    seralized_user = user.serialize()
    return jsonify(seralized_user), 201


@api.route("/favorite/planet/<int:planet_id>", methods=["DELETE"])
def delete_favorite_planet(planet_id):
    body = request.json
    if body is None or "user_id" not in body:
        return jsonify({"message": "Please enter a user_id into the body."}), 400
    user = db.session.get(User, body["user_id"])

    if user is None:
        return jsonify({"message": "invalid user id"}), 404

    # See comment above in the other DELETE route for explanation on what this code syntax does.
    favorite_planet = db.session.execute(
        select(Favorite_Planet).where(
            (Favorite_Planet.user_id == body["user_id"]) &
            (Favorite_Planet.planet_id == planet_id)
        )
    ).scalar_one_or_none()

    if favorite_planet is None:
        return jsonify({"message": "that planet id is not in this user's favorites"}), 404
    db.session.delete(favorite_planet)
    db.session.commit()
    seralized_user = user.serialize()
    return jsonify(seralized_user), 201


# Update the database by running the terminal commands:
    # $ pipenv run migrate
    # $ pipenv run upgrade
    # $ pipenv run start
