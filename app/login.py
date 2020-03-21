from flask import (Blueprint, flash)

from . import db

bp = Blueprint('login', __name__, url_prefix='/login')
mongo = db.get_db()


@bp.route('/', methods=('GET', 'POST'))
def login():
    user = mongo.users
    username = user.find_one({'name': 'admin'})
    return username['name']