import uuid

from flask import (Blueprint, request)
from werkzeug.security import check_password_hash, generate_password_hash

from app import utils
from app import app

blueprint = Blueprint('auth', __name__, url_prefix='/auth')


@blueprint.route('/register', methods=['POST'])
@utils.params_check(['username', 'password'])
def register():
    username = request.form.get('username', None)
    password = request.form.get('password', None)
    users = app.mongo.db.users

    if users.find_one({'username': username}) is not None:
        return {'message': '该用户名已被注册'}, 409

    users.insert_one({
        'username': username,
        'password': generate_password_hash(password),
        'userId': uuid.uuid1()
    })
    return {'message': '注册成功'}, 201


@blueprint.route('/login', methods=['POST'])
@utils.params_check(['username', 'password'])
def login():
    username = request.form.get('username', None)
    password = request.form.get('password', None)
    users = app.mongo.db.users
    user = users.find_one({'username': username})

    if user is None:
        return {
            'message': '用户未注册'
        }, 406

    if not check_password_hash(user['password'], password):
        return {
            'message': '密码错误'
        }, 403

    user_id = user['userId']
    token = utils.create_token(user_id)
    return {
        'message': '登录成功',
        'data': {
            'token': token,
            'user_id': user_id
        }
    }


@blueprint.route('/logout', methods=['POST'])
def logout():
    return {'message': '登出成功'}
