from test import utils
from app.utils import http_code

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


def test_register(client, app):
    # 缺少参数
    assert client.post("/auth/register").status_code == http_code['BadRequest']
    assert client.post("/auth/register", data=user_incomplete_info).status_code == http_code['BadRequest']

    # 成功注册
    assert client.post("/auth/register", data=user_complete_info).status_code == http_code['Created']

    # 用户名重复
    assert client.post("/auth/register", data=user_complete_info).status_code == http_code['Conflict']

    # 清理数据库
    utils.clear_db()


def test_login(client, app):
    response = client.post('/auth/register', data=user_complete_info)

    # 缺少参数
    assert client.post("/auth/register").status_code == http_code['BadRequest']

    # 密码错误
    assert client.post("/auth/login", data=user_wrong_password_info).status_code == http_code['Forbidden']

    # 用户未注册
    assert client.post("/auth/login", data=user_not_found_info).status_code == http_code['Not Acceptable']

    # 成功登录
    assert client.post("/auth/login", data=user_complete_info).status_code == http_code['OK']

    # 清理数据库
    utils.clear_db()


def test_logout(client, app):
    assert client.post("/auth/logout").status_code == http_code['OK']
