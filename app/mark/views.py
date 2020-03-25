import uuid

from flask import (Blueprint, request)

from app import extensions
from app import utils

blueprint = Blueprint('mark', __name__, url_prefix='/mark')


@blueprint.route('/book/add', methods=['POST'])
@utils.token_required
@utils.params_check(['userId', 'bookName'])
def book_add():
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
        # 如果被提交的书籍不存在于书籍收藏的数组里，那么将其添加进去
        if len(
                list(
                    filter(lambda n: n == book_name,
                           result['bookCollections']))) == 0:
            result['bookCollections'].append(book_name)
            collections.update(condition, result)
        else:
            return {'msg': '不可重复收藏'}

    return {'msg': '收藏成功'}


@blueprint.route('/book/del', methods=['POST'])
@utils.token_required
@utils.params_check(['userId', 'bookName'])
def book_del():
    user_id = request.values.get('userId')
    book_name = request.values.get('bookName')
    collections = extensions.get_db().collections
    condition = {'userId': uuid.UUID(user_id)}
    result = collections.find_one(condition)

    result['bookCollections'] = list(
        filter(lambda n: n != book_name, result['bookCollections']))
    collections.update(condition, result)

    return {'msg': '删除成功'}


@blueprint.route('/book/fetch', methods=['POST'])
@utils.token_required
@utils.params_check(['userId'])
def book_fetch():
    user_id = request.values.get('userId')
    collections = extensions.get_db().collections
    condition = {'userId': uuid.UUID(user_id)}
    result = collections.find_one(condition)

    if result:
        return {'msg': '请求成功', 'data': result['bookCollections']}
    else:
        return {'msg': '暂无数据'}


@blueprint.route('/reading/modify', methods=['POST'])
@utils.token_required
@utils.params_check(['userId', 'bookName', 'chapterId'])
def reading_modify():
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
            filter(lambda n: n['bookName'] == book_name, result['bookMarks']))
        try:
            theMark = theMark[0]
        except IndexError:
            result['bookMarks'].append({
                'bookName': book_name,
                'chapterMarks': chapter_id
            })
            collections.update(condition, result)
        else:
            theMark['chapterMarks'] = chapter_id
            collections.update(condition, result)

    return {'msg': '收藏成功'}


@blueprint.route('/reading/fetch', methods=['POST'])
@utils.token_required
@utils.params_check(['userId'])
def reading_fetch():
    user_id = request.values.get('userId')
    collections = extensions.get_db().mark
    condition = {'userId': uuid.UUID(user_id)}
    result = collections.find_one(condition)

    if result:
        return {'msg': '请求成功', 'data': result['bookMarks']}
    else:
        return {'msg': '暂无数据'}
