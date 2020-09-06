import uuid

from flask import (Blueprint, request)

from app import app
from app import utils
from app import extensions

blueprint = Blueprint('mark', __name__, url_prefix='/mark')


@blueprint.route("/book", methods=["POST"])
# @utils.token_required
@utils.params_check(["userId", "bookName"])
def book_add():
    # TODO: 修复前端登录后 user_id 解码 token
    # token_data = utils.verify_token(request.headers['Authorization'])
    # user_id = uuid.UUID(token_data['userId'])
    user_id = request.values.get("userId")
    book_name = request.values.get("bookName")

    collections = app.mongo.db.collections
    condition = {"userId": user_id, "bookName": book_name}
    result = collections.find_one(condition)

    if result is not None:
        return {
            "message": "不可重复收藏"
        }, utils.http_code["Conflict"]

    collections.insert_one({
        "userId": user_id,
        "bookName": book_name
    })

    return {
        "message": "收藏成功",
    }


@blueprint.route("/book", methods=["DELETE"])
# @utils.token_required
@utils.params_check(["bookName"])
def book_del():
    # token_data = utils.verify_token(request.headers['Authorization'])
    # user_id = token_data['userId']
    user_id = request.values.get("userId")
    book_name = request.values.get("bookName")

    collections = app.mongo.db.collections
    condition = {"user_id": user_id, "bookName": book_name}
    collections.delete_one(condition)

    return {"message": "已取消收藏"}


@blueprint.route('/book/fetch', methods=['POST'])
@utils.token_required
def book_fetch():
    token_data = utils.verify_token(request.headers['Authorization'])
    user_id = token_data['userId']
    collections = extensions.get_db().collections
    condition = {'userId': uuid.UUID(user_id)}
    result = collections.find_one(condition)

    # 获取第一本书的图片
    # TODO: 此处实现与前端页面的耦合严重，待修改
    try:
        firstBook = result['bookCollections'][0]
    except IndexError:
        return {'msg': '暂无数据'}
    else:
        books = extensions.get_db().books
        condition = {'bookName': firstBook}
        book = books.find_one(condition)
        book_img = book['imageUrl']
        book_des = book['bookSimpleDes']

        data = {
            'bookCollections': result['bookCollections'],
            'firstBookImg': book_img,
            'firstBookDes': book_des
        }

    if result:
        return {'msg': '请求成功', 'data': data}
    else:
        return {'msg': '暂无数据'}


@blueprint.route('/reading/modify', methods=['POST'])
@utils.token_required
@utils.params_check(['bookName', 'chapterId'])
def reading_modify():
    token_data = utils.verify_token(request.headers['Authorization'])
    user_id = token_data['userId']
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
        # 如果存在该本书的收藏记录，则更新它
        # 如果不存在，则创建
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
def reading_fetch():
    token_data = utils.verify_token(request.headers['Authorization'])
    user_id = token_data['userId']
    collections = extensions.get_db().mark
    condition = {'userId': uuid.UUID(user_id)}
    result = collections.find_one(condition)
    book_name = result['bookMarks'][0]['bookName']

    book_collections = extensions.get_db().books
    book = book_collections.find({
            'bookName': {
                '$regex': book_name
            }
        }, {
            '_id': False
        })[0]
    book_img = book['imageUrl']
    book_des = book['bookSimpleDes']

    data = {
        'bookRecentReading': result['bookMarks'],
        'firstRecordImg': book_img,
        'firstRecordDes': book_des
    }

    if result:
        return {'msg': '请求成功', 'data':  data}
    else:
        return {'msg': '暂无数据'}
