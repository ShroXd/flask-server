from flask import Flask
from flask_pymongo import PyMongo

from . import app


def get_db():
    mongo = PyMongo(app.create_app())

    return mongo.db