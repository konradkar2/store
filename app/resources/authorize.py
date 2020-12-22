from flask_jwt_extended import get_jwt_claims
from app.exceptions import UnauthorizedError
admin = "admin"

def require_admin(func):
    def authorize_and_call(*args, **kwargs):
        claims = get_jwt_claims()
        if claims['role'] == admin:
            return func(*args, **kwargs)
        else:
            raise UnauthorizedError()
   
    return authorize_and_call