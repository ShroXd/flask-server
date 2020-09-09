import math

from flask import (Blueprint, request)

from app import app
from app import utils

blueprint = Blueprint('novel', __name__, url_prefix='/novel')


@blueprint.route('/books', methods=['GET'])
# @utils.token_required
@utils.params_check(['listPage', 'listLimit'])
def novels():
    book_name = str(request.args.get('bookName', ""))
    list_page = int(request.args.get('listPage', 0))
    list_limit = int(request.args.get('listLimit', 0))

    if list_page == 0 or list_limit == 0:
        return {
            "message": "参数错误"
        }, utils.http_code["BadRequest"]

    collections = app.mongo.db.books

    results = collections.find({
        'bookName': {
            '$regex': book_name
        }
    }, {
        '_id': False
    }).skip((list_page - 1) * list_limit).limit(list_limit)

    count_of_result = collections.count_documents({
        'bookName': {
            '$regex': book_name
        }
    })

    num = math.floor(count_of_result / list_limit)

    if count_of_result == 0:
        return {
            "message": "书籍不存在"
        }, utils.http_code["Not Found"]

    return {
        "message": "请求成功",
        "data": {
            "total": num if num != 0 else 1,
            "books": [x for x in results]
        }
    }


@blueprint.route('/chapters', methods=['GET'])
# @utils.token_required
@utils.params_check(['bookName'])
def chapters():
    book_name = str(request.values.get('bookName'))
    collections = app.mongo.db.chapters

    results = collections.find_one({'bookName': book_name}, {'_id': False})

    # TODO 字段命名需规范
    if results is None:
        return {
            "message": "章节不存在"
        }, utils.http_code["Not Found"]

    return {"message": "请求成功", "data": results}


@blueprint.route('/contents', methods=['GET'])
# @utils.token_required
@utils.params_check(['bookName', 'chapterId'])
def contents():
    book_name = str(request.values.get('bookName'))
    chapter_id = str(request.values.get('chapterId'))
    collections = app.mongo.db.contents

    results = collections.find_one(
        {
            'bookName': book_name,
            'chapterId': chapter_id
        }, {'_id': False})

    if results is None:
        return {
            "message": "内容不存在"
        }, utils.http_code["Not Found"]

    return {"message": "请求成功", "data": results}
