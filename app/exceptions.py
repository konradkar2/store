from werkzeug.exceptions import HTTPException
class InternalServerError(HTTPException):
    def __init__(self,err = None):
        super().__init__()
        self.err = err

errors = {
    'InternalServerError': {
        'message': "Internal server error",
        'status': 500,
    },
    
}