from app.utils import http_code


def test_novels(client, app):
    # 缺少参数
    assert client.get("/novel/books").status_code == http_code['BadRequest']

    # 错误参数
    assert client.get("/novel/books?listPage=0&&listLimit=0").status_code == http_code['BadRequest']
    assert client.get("/novel/books?bookName=理想的女儿是世界最强，你也愿意宠爱吗？&&listPage=0&&listLimit=0").status_code == http_code[
        'BadRequest']

    # 正确请求
    assert client.get("/novel/books?listPage=1&&listLimit=10").status_code == http_code['OK']
    assert client.get("/novel/books?bookName=理想的女儿是世界最强，你也愿意宠爱吗？&&listPage=1&&listLimit=10").status_code == http_code[
        'OK']


def test_chapters(client, app):
    # 缺少参数
    assert client.get("/novel/chapters").status_code == http_code['BadRequest']

    # 错误参数
    assert client.get("/novel/chapters").status_code == http_code['BadRequest']
    assert client.get("/novel/chapters?bookName=afwfaewfwaefwae").status_code == http_code['Not Found']

    # 正确请求
    assert client.get("/novel/chapters?bookName=理想的女儿是世界最强，你也愿意宠爱吗？").status_code == http_code['OK']


def test_contents(client, app):
    # 缺少参数
    assert client.get("/novel/contents").status_code == http_code['BadRequest']

    # 错误参数
    assert client.get("/novel/contents?bookName=理想的女儿是世界最强，你也愿意宠爱吗？").status_code == http_code['BadRequest']
    assert client.get("/novel/contents?bookName=理想的女儿是世界最强，你也愿意宠爱吗？&&chapterId=554353").status_code == http_code['Not Found']

    # 正确请求
    assert client.get("/novel/contents?bookName=理想的女儿是世界最强，你也愿意宠爱吗？&&chapterId=70689337").status_code == http_code['OK']