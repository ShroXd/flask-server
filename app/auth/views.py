import uuid

from flask import (Blueprint, request)
from werkzeug.security import check_password_hash, generate_password_hash

from app import extensions
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
    return {'message': '注册成功'}


@blueprint.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = extensions.get_db().users
        msg = None
        user = user.find_one({'username': username})

        if user is None:
            msg = '用户名错误'
        elif not check_password_hash(user['password'], password):
            msg = '密码错误'

        if msg is None:
            # session.clear()
            # session['user_id'] = user['username']
            user_id = user['userId']
            token = utils.create_token(user_id)
            # user = utils.verify_token(token)
            return {'msg': '登录成功', 'token': token, 'userId': user_id}
        else:
            return {'msg': msg}


@blueprint.route('/logout')
def logout():
    session.clear()
    return {'msg': '登出成功'}
