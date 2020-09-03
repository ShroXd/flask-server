from app import app as flaskapp


def test_register(client, app):
    user_complete_info = {
        "username": "test_username",
        "password": "test_password"
    }
    user_incomplete_info = {
        "username": "test_username"
    }

    # 缺少参数
    assert client.post("/auth/register").status_code == 400
    assert client.post("/auth/register", data=user_incomplete_info).status_code == 400

    # 成功注册
    assert client.post("/auth/register",data=user_complete_info).status_code == 200

    # 用户名重复
    assert client.post("/auth/register",data=user_complete_info).status_code == 409

    # 清理数据库
    users = flaskapp.mongo.db.users
    users.delete_one(user_incomplete_info)
