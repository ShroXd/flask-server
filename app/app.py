from flask import Flask

from app import auth, user, novel
from app.settings import DevelopmentConfig


def create_app():
    """An application factory"""

    app = Flask(__name__)

    app.config.from_object(DevelopmentConfig)
    register_blueprints(app)

    return app

def register_blueprints(app):
    """Register Flask blueprints"""

    app.register_blueprint(auth.views.blueprint)
    app.register_blueprint(user.views.blueprint)
    app.register_blueprint(novel.views.blueprint)