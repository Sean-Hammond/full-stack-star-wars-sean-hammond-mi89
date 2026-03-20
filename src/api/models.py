from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

db = SQLAlchemy()


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    favorite_characters: Mapped[List["Favorite_Character"]] = relationship(
        back_populates="user")
    favorite_planets: Mapped[List["Favorite_Planet"]
                             ] = relationship(back_populates="user")
    # favorite_species: Mapped[List["Favorite_Species"]
    #                          ] = relationship(back_populates="user")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }


class Character(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    mass: Mapped[int] = mapped_column(nullable=False)
    height: Mapped[int] = mapped_column(nullable=False)
    age: Mapped[int] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(
        String(500), unique=True, nullable=False)
    planet_id: Mapped[int] = mapped_column(ForeignKey("planet.id"))
    users_who_favorite: Mapped[List["Favorite_Character"]] = relationship(
        back_populates="character")
    planet: Mapped["Planet"] = relationship(back_populates="characters")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "mass": self.mass,
            "height": self.height,
            "age": self.age,
            "description": self.description,
            "planet": self.planet.serialize()
            # do not serialize the password, its a security breach
        }


class Planet(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    mass: Mapped[int] = mapped_column(nullable=False)
    circumference: Mapped[int] = mapped_column(nullable=False)
    characters: Mapped[List["Character"]] = relationship(
        back_populates="planet")
    description: Mapped[str] = mapped_column(
        String(500), unique=True, nullable=False)
    users_who_favorite: Mapped[List["Favorite_Planet"]
                               ] = relationship(back_populates="planet")
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "mass": self.mass,
            "circumference": self.circumference,
            "description": self.description,
            # do not serialize the password, its a security breach
        }


# class Species(db.Model):
#     id: Mapped[int] = mapped_column(primary_key=True)
#     name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
#     description: Mapped[str] = mapped_column(
#         String(500), unique=True, nullable=False)
#     characters: Mapped[List["Character"]] = relationship(
#         back_populates="author")
#     planets: Mapped[List["Planet"]] = relationship(back_populates="author")
#     users_who_favorite: Mapped[List["Favorite_Species"]
#                                ] = relationship(back_populates="species")


class Favorite_Character(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    character_id: Mapped[int] = mapped_column(ForeignKey("character.id"))
    user: Mapped["User"] = relationship(back_populates="favorite_characters")
    character: Mapped["Character"] = relationship(
        back_populates="users_who_favorite")


class Favorite_Planet(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    planet_id: Mapped[int] = mapped_column(ForeignKey("planet.id"))
    user: Mapped["User"] = relationship(back_populates="favorite_planets")
    planet: Mapped["Planet"] = relationship(
        back_populates="users_who_favorite")


# class Favorite_Species(db.Model):
#     id: Mapped[int] = mapped_column(primary_key=True)
#     user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
#     species_id: Mapped[int] = mapped_column(ForeignKey("species.id"))
#     user: Mapped["User"] = relationship(back_populates="favorite_species")
#     species: Mapped["Species"] = relationship(
#         back_populates="users_who_favorite")
    
# Note about the previous project (https://github.com/Sean-Hammond/datamodel-starwars-sean-hammond-mi89), in case same applies here:
# Terminal code to run if the pipenv run migrate gives a Flask error:
    # rm -R -f ./migrations &&
    # pipenv run init &&
    # dropdb -h localhost -U gitpod example || true &&
    # createdb -h localhost -U gitpod example || true &&
    # psql -h localhost example -U gitpod -c 'CREATE EXTENSION unaccent;' || true &&
    # pipenv run migrate &&
    # pipenv run upgrade