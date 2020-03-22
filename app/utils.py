import functools

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
""" def login_required(views_func):
    @functools.wraps(views_func)
    def verify_token(*args,**kwargs):
        try:
            token = request.headers["z-token"]
        except Exception:
            return {'msg': '缺少 token'}
        
        verify = verify_token(token)

        if not verify:
            return {'msg': '登录已过期'}
            
        return views_func(*args,**kwargs)

    return verify_token """

def token_required(request):
    def decorate(func):
        def token_handle(*args, **kwargs):
            try:
                token = request.headers['z-token']
            except Exception:
                return {'msg': '缺少 token'}
            
            _ = verify_token(token)

            if not _:
                return {'msg': '登录已过期'}

            func(*args, **kwargs)
        return token_handle
    return decorate