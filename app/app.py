from flask import Flask

from app import auth, user, novel, mark
from app.settings import DevelopmentConfig, TestConfig

from flask_pymongo import PyMongo

mongo = PyMongo()


def create_app():
    """An application factory"""

    app = Flask(__name__)

    app.config.from_object(DevelopmentConfig)
    register_blueprints(app)

    mongo.init_app(app)

    return app


def create_test_app():
    """An test application factory"""

    app = Flask(__name__)

    app.config.from_object(TestConfig)
    register_blueprints(app)

    mongo.init_app(app)

    return app


def register_blueprints(app):
    """Register Flask blueprints"""

    app.register_blueprint(auth.views.blueprint)
    app.register_blueprint(user.views.blueprint)
    app.register_blueprint(novel.views.blueprint)
    app.register_blueprint(mark.views.blueprint)