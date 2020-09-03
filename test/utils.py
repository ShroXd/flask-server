from app import app as flaskapp
from app.utils import create_token
from app.settings import TestConfig

from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

user_complete_info = {
    "username": "test_username",
    "password": "test_password"
}
user_incomplete_info = {
    "username": "test_username"
}
user_wrong_password_info = {
    "username": "test_username",
    "password": "wrong_password"
}
user_not_found_info = {
    "username": "not_found",
    "password": "password"
}


def clear_db():
    users = flaskapp.mongo.db.users
    users.delete_one(user_incomplete_info)


def fetch_token():
    users = flaskapp.mongo.db.users
    user_id = users.find_one(user_incomplete_info)['userId']
    # print(user_id)

    s = Serializer(TestConfig.SECRET_KEY, expires_in=TestConfig.TOKEN_EXPIRES)
    token = s.dumps({"userId": str(user_id)}).decode("ascii")

    return token
