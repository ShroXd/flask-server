from test import utils


def test_info(client, app):
    client.post('/auth/register', data=utils.user_complete_info)

    # 缺少 token
    assert client.post("/auth/register").status_code == 400

    # 使用正确 token 获取用户信息
    token = utils.fetch_token()
    assert client.get("/user/info", headers={"Authorization": token}).status_code == 200

    # 使用错误 token 获取用户信息
    assert client.get("/user/info", headers={"Authorization": "wrong token"}).status_code == 401

    # 清理数据库
    utils.clear_db()
