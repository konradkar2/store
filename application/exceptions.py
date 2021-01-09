from werkzeug.exceptions import HTTPException
class InternalServerError(HTTPException):
    def __init__(self,err = None):
        super().__init__()
        self.err = err

class BadRequestError(HTTPException):
    pass
class UnauthorizedError(HTTPException):
    pass
errors = {
    'InternalServerError': {
        'message': "Internal server error",
        'status': 500,
    },
    'BadRequestError': {
        'message' : 'Bad request error',
        'status' : 400
    },
    'UnauthorizedError': {
        'message' : "Unauthorized error",
        'status' : 401
    }
}