from flask import Flask


def create_app():
    from . import login
    app = Flask(__name__, instance_relative_config=True)

    app.register_blueprint(login.bp)

    return app