from flask_restful import Resource, reqparse
import mysql.connector
from flask_jwt_extended import jwt_required,get_jwt_identity
from datetime import datetime
from cerberus import Validator
import json

from store.application.models.game import GameModel
from store.application.models.game_transaction import GameTransactionModel
from store.application.models.user_transaction import UserTransactionModel
from store.application.models.key import KeyModel
from store.application.models.category import CategoryModel
from store.application.models.platform import PlatformModel
from store.application.exceptions import InternalServerError, BadRequestError
from store.application.utils.db import dbCursor

def shopping_cart_validator(value):
    CART_SCHEMA = {
        'game_id': {'required': True, 'type': 'integer'},
        'quantity': {'required': True, 'type': 'integer'}
    }
    v = Validator(CART_SCHEMA)
    if v.validate(value):
        return value
    else:
        raise ValueError(json.dumps(v.errors))

def search_filter_validator(value):
    filter_schema = {
        'title' : {'required': False, 'type' : 'string'},
        'categories_id' : {'required' : False, 'type' : ['integer','list']},
        'platforms_id' : {'required' : False, 'type' : ['integer','list']},
        'order_by' : {'required' : False, 'type': 'string', 'allowed' : ['price','name']},
        'order_rule' :{'required' : False, 'type': 'string', 'allowed' : ['asc','desc']}
    }
    v = Validator(filter_schema)
    if v.validate(value):
        return value
    else:
        raise ValueError(json.dumps(v.errors))

class AdvancedSearchGame(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('search_filter', type=search_filter_validator)

    @classmethod
    def post(cls):
        try:
            data = cls.parser.parse_args()       
            if data['search_filter'] is None:
                return {'message' : 'Search filter cannot be empty'},400
            
            print(data)
            return 200

        except Exception as e:
            raise InternalServerError(e)
        



class SearchGame(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "title", type=str, required=True, location='args',help="This field cannot be left blank!"
    )
    @classmethod
    def get(cls):
        data = cls.parser.parse_args()        
        try:
            with dbCursor() as cursor:
                games = GameModel.find_many_by_name(cursor,data['title'])         
                return {
                    'result_count' : len(games),
                    'games' : [game.json() for game in games]}
        except Exception as e:
            raise InternalServerError(e)


class FetchCategories(Resource):
    @classmethod
    def get(cls):       
        try:
            with dbCursor() as cursor:
                categories = CategoryModel.find_all(cursor)    
                return {                
                    'categories' : [category.json() for category in categories]}
        except Exception as e:
            raise InternalServerError(e)


class FetchPlatforms(Resource):
    @classmethod
    def get(cls):       
        try:
            with dbCursor() as cursor:
                platforms = PlatformModel.find_all(cursor)    
                return {                
                    'platforms' : [platform.json() for platform in platforms]}
        except Exception as e:
            raise InternalServerError(e)

class FetchGame(Resource):
    @classmethod
    def get(cls,game_id):
        try:
            with dbCursor() as cursor:
                game = GameModel.find_by_id(cursor,game_id)    
                if game is None:
                    return {"message" : "Game of id {_id} not found.".format(_id=game_id)}, 404
                
                return { "game" : game.json() }
        except Exception as e:
            raise InternalServerError(e)
        


class BuyGames(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('shopping_cart', type=shopping_cart_validator, action='append')

    @classmethod
    @jwt_required
    def post(cls):
        data = cls.parser.parse_args()    
        try:
            with dbCursor() as cursor:
                #verify data  
                if len(data['shopping_cart']) == 0:
                    return {"message" : "Shopping cannot be empty"}, 400

                for entry in data['shopping_cart']:
                    game_id = entry['game_id']
                    quantity = entry['quantity']

                    game = GameModel.find_by_id(cursor,game_id)
                    if game is None:
                        return {"message" : "Game of id {game_id} not found.".format(game_id=game_id)}, 400
                    quantity_in_db = game.get_quantity(cursor)
                    
                    if quantity_in_db < quantity:
                        return {"message" : "Game of id {game_id} is available only in {quantity} pieces.".format(game_id=game_id,quantity=quantity_in_db)}, 400
                
                #data is partially verified, now some bad asynch stuff might happen
                
                user_id = get_jwt_identity()
                date = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
                userTransaction = UserTransactionModel(user_id,date)
                userTransaction.save_to_db(cursor)

                user_transaction_id = userTransaction.id # this is not user_id, TODO: change its name for less ambigous
                for entry in data['shopping_cart']:
                    game_id = entry['game_id']
                    quantity = entry['quantity']
                    
                    key = KeyModel.find_any_not_used(cursor,game_id)
                    keyId = key.id
                    gameTransaction = GameTransactionModel(user_transaction_id,game_id,keyId)
                    gameTransaction.save_to_db(cursor)
                    
                return {'message': 'Games purchase successful'}, 201
        except Exception as e:
            raise InternalServerError(e)

