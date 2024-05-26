from functools import wraps
from flask import request, jsonify
import utils.my_jwt as my_jwt

jwt = my_jwt.MyJwt()


def jwt_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"message": "Token is missing"}), 401
        sign = jwt.parse_token(token)
        if sign != True:
            return jsonify({"message": sign}), 401
        response = f(*args, **kwargs)
        return response

    return decorated_function
