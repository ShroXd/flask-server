from test import utils
from app.utils import http_code


def test_info(client, app):
    client.post('/auth/register', data=utils.user_complete_info)

    # 缺少 token
    assert client.post("/auth/register").status_code == http_code['BadRequest']

    # 使用正确 token 获取用户信息
    token = utils.fetch_token()
    assert client.get("/user/info", headers={"Authorization": token}).status_code == http_code['OK']

    # 使用错误 token 获取用户信息
    assert client.get("/user/info", headers={"Authorization": "wrong token"}).status_code == http_code['Unauthorized']

    # 清理数据库
    utils.clear_db()
