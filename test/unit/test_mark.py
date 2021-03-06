from test import utils
from app.utils import http_code
from app import app as flaskapp


def test_book_add(client, app):
    flaskapp.mongo.db.collections.drop()

    # 缺少参数
    assert client.post("/mark/book").status_code == http_code["BadRequest"]
    assert client.post("/mark/book", data={"bookName": "妹妹"}).status_code == http_code["BadRequest"]

    # 成功提交收藏
    assert client.post("/mark/book", data={"bookName": "妹妹", "userId": "123456"}).status_code == http_code["OK"]

    # 清理数据库
    flaskapp.mongo.db.collections.drop()


def test_book_del(client, app):
    # 缺少参数
    assert client.delete("/mark/book").status_code == http_code["BadRequest"]

    # 成功删除收藏
    client.post("/mark/book", data={"bookName": "妹妹", "userId": "123456"})
    assert client.delete("/mark/book", data={"bookName": "妹妹", "userId": "123456"}).status_code == http_code["OK"]


def test_book_fetch(client, app):
    # 成功获取收藏
    flaskapp.mongo.db.collections.drop()
    client.post("/mark/book", data={"bookName": "妹妹", "userId": "123456"})
    assert client.get("/mark/book?userId=123456").status_code == http_code["OK"]
    assert client.get("/mark/book?bookName=妹妹&&userId=123456").status_code == http_code["OK"]


def test_reading_modify(client, app):

    # 成功添加阅读记录
    assert client.post("/mark/reading", data={"userId": "123456", "bookName": "妹妹", "chapterId": "7890"}).status_code == http_code["OK"]

    # 不可重复收藏
    assert client.post("/mark/reading", data={"userId": "123456", "bookName": "妹妹", "chapterId": "7890"}).status_code == http_code["Conflict"]

    # 清理数据库
    flaskapp.mongo.db.mark.drop()


def test_reading_fetch(client, app):
    # 成功获取阅读记录
    flaskapp.mongo.db.mark.drop()
    client.post("/mark/reading", data={"userId": "123456", "bookName": "妹妹", "chapterId": "7890"})
    assert client.get("/mark/book?userId=123456").status_code == http_code["OK"]
    assert client.get("/mark/book?bookName=妹妹&&userId=123456").status_code == http_code["OK"]

    # 清理数据库
    flaskapp.mongo.db.mark.drop()
