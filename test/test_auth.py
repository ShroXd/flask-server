from app import app as flaskapp

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
    assert client.post("/auth/register").status_code == 400
    assert client.post("/auth/register", data=user_incomplete_info).status_code == 400

    # 成功注册
    assert client.post("/auth/register", data=user_complete_info).status_code == 201

    # 用户名重复
    assert client.post("/auth/register", data=user_complete_info).status_code == 409

    # 清理数据库
    users = flaskapp.mongo.db.users
    users.delete_one(user_incomplete_info)


def test_login(client, app):
    response = client.post('/auth/register', data=user_complete_info)

    # 缺少参数
    assert client.post("/auth/register").status_code == 400

    # 密码错误
    assert client.post("/auth/login", data=user_wrong_password_info).status_code == 403

    # 用户未注册
    assert client.post("/auth/login", data=user_not_found_info).status_code == 406

    # 成功登录
    assert client.post("/auth/login", data=user_complete_info).status_code == 200

    # 清理数据库
    users = flaskapp.mongo.db.users
    users.delete_one(user_incomplete_info)


def test_logout(client, app):
    assert client.post("/auth/logout").status_code == 200
