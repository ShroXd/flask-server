from flask import Flask


def create_app():
    from . import auth
    app = Flask(__name__, instance_relative_config=True)

    # 支持中文显示
    app.config['JSON_AS_ASCII'] = False
    # session 的秘钥
    app.secret_key = 'djskla'

    app.register_blueprint(auth.bp)

    return app