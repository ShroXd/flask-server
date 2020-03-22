from flask import request, jsonify, current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


# 生成 token
def create_token(request_user):

    s = Serializer(current_app.config["SECRET_KEY"], expires_in=3600)
    token = s.dumps({"username": request_user}).decode("ascii")
    return token


# 校验 token
def verify_token(token):

    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except Exception:
        return None
    else:
        return data


# 请求必须携带 token 的校验装饰器