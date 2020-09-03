import functools

from flask import request, jsonify, current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from app.settings import DevelopmentConfig

# http code 对照表
http_code = {
    "OK": 200,
    "Created": 201,
    "BadRequest": 400,
    "Unauthorized": 401,
    "Forbidden": 403,
    "Not Acceptable": 406,
    "Conflict": 409
}


# 生成 token
def create_token(request_user):
    s = Serializer(current_app.config["SECRET_KEY"], expires_in=DevelopmentConfig.TOKEN_EXPIRES)
    token = s.dumps({"userId": str(request_user)}).decode("ascii")
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
def token_required(func):
    @functools.wraps(func)
    def token_handle(*args, **kwargs):
        try:
            token = request.headers['Authorization']
        except Exception:
            return {'message': '缺少 token'}, http_code['Unauthorized']

        _ = verify_token(token)

        if not _:
            return {'message': '登录已过期'}, http_code['Unauthorized']
        return func(*args, **kwargs)

    return token_handle


# request 请求参数检查装饰器
def params_check(params_list):
    def decotate(func):
        @functools.wraps(func)
        def check(*args, **kwargs):
            for _ in params_list:
                if not request.values.get(str(_)):
                    return {'message': '缺少参数'.format(str(_))}, http_code['BadRequest']

            return func(*args, **kwargs)

        return check

    return decotate