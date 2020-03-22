from flask import (Blueprint, request, jsonify, session)
from werkzeug.security import check_password_hash, generate_password_hash

from app import extensions

blueprint = Blueprint('auth', __name__, url_prefix='/auth')


@blueprint.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form.get('username', None)
        password = request.form.get('password', None)
        user = extensions.get_db().users
        msg = None

        if not username:
            msg = '请输入用户名'
        elif not password:
            msg = '请输入密码'
        elif user.find_one({'username': username}) is not None:
            msg = '用户 {} 已注册'.format(username)

        if msg is None:
            user.insert({
                'username': username,
                'password': generate_password_hash(password)
            })
            return jsonify({'msg': '注册成功'})
        else:
            return jsonify({'msg': msg})


@blueprint.route('/login', methods=('POST', 'GET'))
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
            session.clear()
            session['user_id'] = user['username']
            return {'msg': '登录成功'}
        else:
            return {'msg': msg}


@blueprint.route('/logout')
def logout():
    session.clear()
    return {'msg': '登出成功'}
