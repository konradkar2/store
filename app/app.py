from flask import Flask,got_request_exception
from flask_restful import Resource, Api
import logging


from exceptions import errors
from resources.user import UserRegister

root_logger= logging.getLogger()
root_logger.setLevel(logging.DEBUG) 
handler = logging.FileHandler('app-errors.log', 'a', 'utf-8') 
handler.setFormatter(logging.Formatter('%(asctime)s %(message)s')) 
root_logger.addHandler(handler)

def log_exception(sender, exception, **extra):
    """ Log an exception to our logging framework """    
    root_logger.error(exception)
    try:
        root_logger.error(exception.err)
    except AttributeError:
        pass

app = Flask(__name__)
got_request_exception.connect(log_exception, app)

api = Api(app,errors=errors)

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

api.add_resource(HelloWorld, '/')
api.add_resource(UserRegister,'/register')

if __name__ == '__main__':
    app.run(debug=True)