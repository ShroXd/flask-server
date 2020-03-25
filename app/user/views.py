import uuid

from flask import (Blueprint, request)

from app import extensions
from app import utils

blueprint = Blueprint('user', __name__, url_prefix='/user')


@blueprint.route('/info', methods=['GET'])
@utils.token_required
def info():
    token = request.headers['Authorization']
    user_data = utils.verify_token(token)
    collections = extensions.get_db().users

    result = collections.find_one({'userId': uuid.UUID(user_data['userId'])})
    return {
        'msg': '请求成功',
        'data': {
            'username': result['username'],
            'userId': result['userId']
        }
    }