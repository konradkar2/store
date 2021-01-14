from flask import Flask,jsonify,got_request_exception
from flask_cors import CORS
from flask_restful import Resource, Api
from flask_jwt_extended import JWTManager
import logging
import traceback
import sys


from store.application.exceptions import errors
from store.application.resources.user import UserRegister, UserLogin, ChangePassword, ChangeEmail, AdminRegister, ChangeRole
from store.application.resources.game_admin import AddGame, AddKey, AddCategory, DeleteCategory, AddPlatform, DeletePlatform, FetchAllShoppings, FetchAllUsers
from store.application.resources.game_public import AdvancedSearchGame,BuyGames,FetchCategories,FetchGame,FetchPlatforms,FetchMyShoppings
from store.application.resources.jwt import set_jwt_settings


root_logger= logging.getLogger()
root_logger.setLevel(logging.DEBUG) 
handler = logging.FileHandler('app-errors.log', 'a', 'utf-8') 
handler.setFormatter(logging.Formatter('%(asctime)s %(message)s')) 
root_logger.addHandler(handler)
root_logger.addHandler(logging.StreamHandler(sys.stdout))

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
CORS(app)
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
api.add_resource(ChangePassword,'/chpass')
api.add_resource(ChangeEmail, '/chemail')
api.add_resource(AdminRegister, '/registeradmin')
api.add_resource(ChangeRole, '/changerole')

api.add_resource(AddGame,'/addgame')
api.add_resource(AdvancedSearchGame,'/games')
api.add_resource(FetchCategories,'/categories')
api.add_resource(FetchPlatforms,'/platforms')
api.add_resource(FetchGame,'/game/<string:game_id>')
api.add_resource(BuyGames,'/buy')
api.add_resource(AddKey,'/addkey')
api.add_resource(AddCategory, '/addcategory/<string:name>')
api.add_resource(DeleteCategory, '/deletecategory/<string:name>')
api.add_resource(AddPlatform, '/addplatform/<string:name>')
api.add_resource(DeletePlatform, '/deleteplatform/<string:name>')
api.add_resource(FetchMyShoppings,'/myshoppings')
api.add_resource(FetchAllShoppings, '/transhistory')
api.add_resource(FetchAllUsers, '/allusers')

if __name__ == '__main__':
    app.run(debug=True)