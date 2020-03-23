from flask import (Blueprint, request)
from app import utils

blueprint = Blueprint('user', __name__, url_prefix='/user')


@blueprint.route('/info', methods=['GET'])
@utils.token_required
def info():
    if request.method == 'GET':
        token = request.headers['Authorization']
        user_data = utils.verify_token(token)
        return {'msg': '请求成功', 'data': {'username': user_data['username']}}
