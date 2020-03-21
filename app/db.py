from flask import Flask
from flask_pymongo import PyMongo


def get_db():
    app = Flask(__name__)
    app.config["MONGO_URI"] = "mongodb://49.232.5.176:34541/dev"
    mongo = PyMongo(app)

    return mongo.db