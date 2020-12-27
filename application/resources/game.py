from flask_restful import Resource, reqparse
import mysql.connector
from flask_jwt_extended import jwt_required,get_jwt_identity
from datetime import datetime

from store.application.models.game import GameModel
from store.application.models.category import CategoryModel
from store.application.models.key import KeyModel
from store.application.resources.authorize import require_admin
from store.application.exceptions import InternalServerError, BadRequestError

class AddGame(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "name", type=str, required=True, help="This field cannot be left blank!"
    )
    parser.add_argument(
        "price", type=float, required=True, help="This field cannot be left blank!"
    )
    parser.add_argument(
        "quantity", type=str,  required=True, help="This field cannot be left blank!"
    )
    parser.add_argument(
        "description", type=str, required=True, help="This field cannot be left blank!"
    )
    parser.add_argument(
        "release_date", type=str, required=True, help="This field cannot be left blank!"
    )
    parser.add_argument(
        "is_digital", type=bool,  required=True, help="This field cannot be left blank!"
    )    
    parser.add_argument(
        "platform_id", type=int, required=True, help="This field cannot be left blank!"
    )
    parser.add_argument(
        "age_category", type=str,  required=True, help="This field cannot be left blank!"
    )
    parser.add_argument(
        "categories", action='append',  required=True, help="This field cannot be left blank!"
    )
    

    @classmethod
    @jwt_required    
    #@require_admin
    def post(cls):
        data = cls.parser.parse_args()  
        try:
            #create and and save GameModel
            now = datetime.utcnow()
            data['release_date'] = now.strftime('%Y-%m-%d %H:%M:%S')
            categories = data.pop('categories')
            game = GameModel(**data)
            game.save_to_db()
            #create categories for the game.id
            if game.id:
                for name in categories:
                    category = CategoryModel(name,game.id)
                    category.save_to_db()
        except mysql.connector.Error as e:
            raise InternalServerError(e)
        except ValueError as e:
            raise BadRequestError()
        except Exception as e:
            raise InternalServerError(e)

        return {'message': 'Game added successfully.'}, 201


class SearchGame(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "title", type=str, required=True, location='args',help="This field cannot be left blank!"
    )
    @classmethod
    def get(cls):
        data = cls.parser.parse_args()        
        try:
            games = GameModel.find_many_by_name(data['title'])         
            return {
                'result_count' : len(games),
                'games' : [game.json() for game in games]}
        except Exception as e:
            raise InternalServerError(e)

class AddKey(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "game_id", type=int,  required=True, help="This field cannot be left blank!"        
    )
    parser.add_argument(
        "key", type=str,  required=True, help="This field cannot be left blank!"     
    )
    
    @jwt_required
    #@require_admin
    def post(cls):
        data = cls.parser.parse_args()  
        key = data['key']    
        game_id = data['game_id']
        try:
            game = GameModel.find_by_id(game_id)
            if game is None:
                return {'message' : "Error when appending key, game id not found"}, 404
            if game.is_digital == False:
                return {'message' : "Error when appending key, game of id {game_id} is not digital".format(game_id=game_id)}, 404
            key = KeyModel.find_by_key(game_id,key)
            if key:
                return {'message' : "Error when appending key, already in database", "key" : key.json()}, 401   

            key = KeyModel(game_id,key)
            key.save_to_db()

            return {'message': 'Key added sucessfully.'}, 201

        except Exception as e:
            raise InternalServerError(e)

