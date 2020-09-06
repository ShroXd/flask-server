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


@blueprint.route("/book", methods=["GET"])
# @utils.token_required
def book_fetch():
    # token_data = utils.verify_token(request.headers['Authorization'])
    # user_id = token_data['userId']
    user_id = request.values.get("userId")
    book_name = request.values.get("bookName", "")

    collections = app.mongo.db.collections
    condition = {"userId": user_id, "bookName": book_name} if book_name != "" else {"userId": user_id}
    result = collections.find(condition, {'_id': False})
    return fetch_data(result)


@blueprint.route("/reading", methods=["POST"])
# @utils.token_required
@utils.params_check(["bookName", "chapterId"])
def reading_modify():
    # token_data = utils.verify_token(request.headers['Authorization'])
    # user_id = token_data['userId']
    user_id = request.values.get("userId")
    book_name = request.values.get('bookName')
    chapter_id = request.values.get('chapterId')

    collections = app.mongo.db.mark
    condition = {"userId": user_id, "bookName": book_name, "chapterId": chapter_id}
    result = collections.find_one(condition)

    if result is not None:
        return {
            "message": "不可重复收藏"
        }, utils.http_code["Conflict"]

    collections.insert_one({
        "userId": user_id,
        "bookName": book_name,
        "chapterId": chapter_id
    })

    return {
        "message": "收藏成功"
    }


@blueprint.route('/reading', methods=['GET'])
# @utils.token_required
# @utils.params_check(["bookName"])
def reading_fetch():
    # token_data = utils.verify_token(request.headers['Authorization'])
    # user_id = token_data['userId']
    user_id = request.values.get("userId")
    book_name = request.values.get("bookName", "")

    collections = app.mongo.db.mark
    condition = {'userId': user_id, 'bookName': book_name} if book_name != "" else {'userId': user_id}
    result = collections.find(condition, {'_id': False})
    return fetch_data(result)


def fetch_data(result):
    result = [x for x in result]

    if len(result) == 0:
        return {
            "message": "暂无数据"
        }, utils.http_code["Not Found"]

    return {
        "message": "获取收藏成功",
        "data": result
    }
