from flask import request,jsonify,current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

# 生成 token

# 校验 token

# 请求必须携带 token 的校验装饰器