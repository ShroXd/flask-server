import math

from flask import (Blueprint, request)

from app import app
from app import utils
from app import extensions

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

    books = app.mongo.db.books

    results = books.find({
        'bookName': {
            '$regex': book_name
        }
    }, {
        '_id': False
    }).skip((list_page - 1) * list_limit).limit(list_limit)

    num = math.floor(results.count() / list_limit)

    if results.count() == 0:
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
    chapter = app.mongo.db.chapters

    results = chapter.find_one({'bookName': book_name}, {'_id': False})

    if results is None:
        return {
            "message": "章节不存在"
        }, utils.http_code["Not Found"]

    return {"message": "请求成功", "data": results}


@blueprint.route('/contents', methods=['POST'])
# @utils.token_required
@utils.params_check(['bookName', 'chapterId'])
def contents():
    book_name = str(request.values.get('bookName'))
    chapter_id = str(request.values.get('chapterId'))
    collections = extensions.get_db().contents

    results = collections.find_one(
        {
            'bookName': book_name,
            'chapterId': chapter_id
        }, {'_id': False})

    return {'msg': '请求成功', 'data': results}
