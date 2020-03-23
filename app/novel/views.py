from bson import json_util
from flask import (Blueprint, request)

from app import extensions
from app import utils

blueprint = Blueprint('novel', __name__, url_prefix='/novel')


@blueprint.route('/books', methods=['POST'])
@utils.token_required
@utils.params_check(['bookName', 'listPage', 'listLimit'])
def books():
    book_name = str(request.values.get('bookName'))
    list_page = int(request.values.get('listPage'))
    list_limit = int(request.values.get('listLimit'))
    collections = extensions.get_db().books

    results = collections.find({}, {'_id': False}).skip(list_page * list_limit).limit(list_limit)
    results_list =  [x for x in results]

    return {'msg': '请求成功', 'data': results_list}


@blueprint.route('/chapters', methods=['POST'])
@utils.token_required
@utils.params_check(['bookName'])
def chapters():
    book_name = str(request.values.get('bookName'))
    collections = extensions.get_db().chapters

    results = collections.find({'bookName': book_name}, {'_id': False})
    results_list = [x for x in results]

    return {'msg': '请求成功', 'data': results_list}


@blueprint.route('/contents', methods=['POST'])
@utils.token_required
@utils.params_check(['chapterId'])
def contents():
    chapter_id = str(request.values.get('chapterId'))
    collections = extensions.get_db().contents

    results = collections.find({'chapterId': chapter_id}, {'_id': False})
    results_list = [x for x in results]

    return {'msg': '请求成功', 'data': results_list}