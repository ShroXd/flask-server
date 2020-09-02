import math

from bson import json_util
from flask import (Blueprint, request)

from app import extensions
from app import utils

blueprint = Blueprint('novel', __name__, url_prefix='/novel')


@blueprint.route('/books', methods=['POST'])
# @utils.token_required
@utils.params_check(['listPage', 'listLimit'])
def books():
    book_name = str(request.values.get('bookName'))
    list_page = int(request.values.get('listPage'))
    list_limit = int(request.values.get('listLimit'))
    collections = extensions.get_db().books
    
    if book_name == '':
        results = collections.find({}, {
            '_id': False
        }).skip((list_page - 1) * list_limit).limit(list_limit)
    else:
        results = collections.find({
            'bookName': {
                '$regex': book_name
            }
        }, {
            '_id': False
        }).skip((list_page - 1) * list_limit).limit(list_limit)

    num = math.floor(results.count() / list_limit) 
    total = num if num != 0 else 1
    results_list = [x for x in results]

    return {'msg': '请求成功', 'data': results_list, 'total': total}


@blueprint.route('/chapters', methods=['POST'])
@utils.token_required
@utils.params_check(['bookName'])
def chapters():
    book_name = str(request.values.get('bookName'))
    collections = extensions.get_db().chapters

    results = collections.find_one({'bookName': book_name}, {'_id': False})
    # results_list = [x for x in results]

    return {'msg': '请求成功', 'data': results}


@blueprint.route('/contents', methods=['POST'])
@utils.token_required
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