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


@blueprint.route('/collections', methods=['POST'])
@utils.token_required
@utils.params_check(['userId', 'bookName'])
def collections():
    user_id = request.values.get('userId')
    book_name = request.values.get('bookName')
    collections = extensions.get_db().collections
    condition = {'userId': uuid.UUID(user_id)}
    result = collections.find_one(condition)

    if not result:
        collections.insert_one({
            'userId': uuid.UUID(user_id),
            'bookCollections': [book_name]
        })
    else:
        result['bookCollections'].append(book_name)
        result['bookCollections'] = list(set(result['bookCollections']))
        collections.update(condition, result)

    return {'msg': '收藏成功'}


@blueprint.route('/bookmark', methods=['POST'])
@utils.token_required
@utils.params_check(['userId', 'bookName', 'chapterId'])
def bookmark():
    user_id = request.values.get('userId')
    book_name = request.values.get('bookName')
    chapter_id = request.values.get('chapterId')
    collections = extensions.get_db().mark
    condition = {'userId': uuid.UUID(user_id)}
    result = collections.find_one(condition)

    if not result:
        collections.insert_one({
            'userId':
            uuid.UUID(user_id),
            'bookMarks': [{
                'bookName': book_name,
                'chapterMarks': chapter_id
            }]
        })
    else:
        theMark = list(
            filter(lambda n: n['bookName'] == book_name,
                   result['bookMarks']))[0]
        theMark['chapterMarks'] = chapter_id
        result['bookMarks'] = theMark
        collections.update(condition, result)

    return {'msg': '收藏成功'}
