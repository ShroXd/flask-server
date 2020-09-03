import uuid

from flask import (Blueprint, request)

from app import app
from app import utils

blueprint = Blueprint('user', __name__, url_prefix='/user')


@blueprint.route('/info', methods=['GET'])
@utils.token_required
def info():
    token = request.headers['Authorization']
    user_data = utils.verify_token(token)
    users = app.mongo.db.users

    result = users.find_one({'userId': uuid.UUID(user_data['userId'])})

    if result is None:
        return {
            "message": "用户不存在"
        }, utils.http_code['BadRequest']

    return {
        'message': '请求成功',
        'data': {
            'username': result['username'],
            'userId': result['userId']
        }
    }