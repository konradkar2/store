from flask import Flask,jsonify,got_request_exception
from flask_restful import Resource, Api
from flask_jwt_extended import JWTManager
import logging
import traceback


from store.application.exceptions import errors
from store.application.resources.user import UserRegister, UserLogin
from store.application.resources.game import AddGame,SearchGame
from store.application.resources.jwt import set_jwt_settings


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
    finally:
        tracelog = traceback.format_exc()
        root_logger.error(tracelog)
        
        
        



app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'tajnykluczyk'
got_request_exception.connect(log_exception, app)

api = Api(app,errors=errors)

jwt = JWTManager(app)

set_jwt_settings(jwt)

class HelloWorld(Resource):
    def get(self):
        return jsonify({'hello': 'world'})

api.add_resource(HelloWorld, '/')
api.add_resource(UserRegister,'/register')
api.add_resource(UserLogin,'/auth')

api.add_resource(AddGame,'/addgame')
api.add_resource(SearchGame,'/games')

if __name__ == '__main__':
    app.run(debug=True)