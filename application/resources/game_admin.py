from flask_restful import Resource, reqparse
import mysql.connector
from flask_jwt_extended import jwt_required,get_jwt_identity
from datetime import datetime

from store.application.models.game import GameModel
from store.application.models.game_category import GameCategoryModel
from store.application.models.category import CategoryModel
from store.application.models.platform import PlatformModel
from store.application.models.key import KeyModel
from store.application.resources.authorize import require_admin
from store.application.exceptions import InternalServerError, BadRequestError
from store.application.models.category import CategoryModel
from store.application.utils.db import dbCursor
from store.application.models.game_transaction import GameTransactionModel
from store.application.models.user_transaction import UserTransactionModel
from store.application.models.user import UserModel

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
        "is_digital", type=lambda x: x if (int(x) == 0 or int(x) == 1) else False,  required=True, help="This field cannot be left blank!"
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
    @require_admin
    def post(cls):
        data = cls.parser.parse_args()  
        try:
            #create and and save GameModel
            now = datetime.utcnow()
            data['release_date'] = now.strftime('%Y-%m-%d %H:%M:%S')
            categories = data.pop('categories')
            with dbCursor() as cursor:
                for category_id in categories:
                    category = CategoryModel.find_by_id(cursor,category_id)
                    if category is None:                        
                        return {'message': 'Category with id {id} not found'.format(id=category_id)}, 404
               
                platform_id = data['platform_id']
                platform = PlatformModel.find_by_id(cursor,platform_id)
                if platform is None:
                    return {'message': 'Platform with id {id} not found'.format(id=platform_id)}, 404

                game = GameModel(**data)            
                game.save_to_db(cursor)
                #create categories for the game.id                
                for category_id in categories:                                      
                    game_category = GameCategoryModel(game.id,category_id)
                    game_category.save_to_db(cursor)
        except mysql.connector.Error as e:
            raise InternalServerError(e)
        except ValueError as e:
            raise BadRequestError()
        except Exception as e:
            raise InternalServerError(e)

        return {'message': 'Game added successfully.'}, 201

class EditGame(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "name", type=str, required=False, help="This field cannot be left blank!"
    )
    parser.add_argument(
        "price", type=float, required=False, help="This field cannot be left blank!"
    )
    parser.add_argument(
        "quantity", type=str, required=False, help="This field cannot be left blank!"
    )
    parser.add_argument(
        "description", type=str, required=False, help="This field cannot be left blank!"
    )
    parser.add_argument(
        "release_date", type=str, required=False, help="This field cannot be left blank!"
    )
    parser.add_argument(
        "is_digital", type=lambda x: x if (int(x) == 0 or int(x) == 1) else False, required=False,
        help="This field cannot be left blank!"
    )
    parser.add_argument(
        "platform_id", type=int, required=False, help="This field cannot be left blank!"
    )
    parser.add_argument(
        "age_category", type=str, required=False, help="This field cannot be left blank!"
    )
    parser.add_argument(
        "categories", action='append', required=False, help="This field cannot be left blank!"
    )
    parser.add_argument(
        "game_id", type=int, required=True, help="This field cannot be left blank!"
    )

    @classmethod
    @jwt_required
    @require_admin
    def post(cls):
        data = cls.parser.parse_args()
        new_name = data["name"]
        new_price = data["price"]
        new_quantity = data["quantity"]
        new_descr = data["description"]
        new_rel_date = data["release_date"]
        new_is_digital = data["is_digital"]
        new_platform = data["platform_id"]
        new_age = data["age_category"]
        new_categories = data["categories"]
        game_id = data["game_id"]
        try:
            # create and and save GameModel
            now = datetime.utcnow()
            new_rel_date = now.strftime('%Y-%m-%d %H:%M:%S')
            with dbCursor() as cursor:
                game = GameModel.find_by_id(cursor, game_id)
                if game:
                    if new_name:
                        game.name = new_name
                    if new_price:
                        game.price = new_price
                    if new_quantity:
                        game.quantity = new_quantity
                    if new_descr:
                        game.description = new_descr
                    if new_descr:
                        game.description = new_descr
                    if new_rel_date:
                        game.release_date = new_rel_date
                    if new_is_digital:
                        if KeyModel.find_all_by_game_id(cursor, game_id) is not None:
                            return {'message': 'Cant change to box, keys for the game exists'}, 404
                        else:
                            game.is_digital = new_is_digital
                    if new_platform:
                        if PlatformModel.find_by_id(cursor, new_platform) is not None:
                            game.platform_id = new_platform
                        else:
                            return {'message': 'Platform doesnt exist'}, 404
                    if new_age:
                        game.age_category = new_age
                    if new_categories:
                        for category_id in new_categories:
                            category = CategoryModel.find_by_id(cursor, category_id)
                            if category is None:
                                return {'message': 'Category with id {id} not found'.format(id=category_id)}, 404
                        GameCategoryModel.delete_by_game_id(cursor, game_id)
                        for category_id in new_categories:
                            game_category = GameCategoryModel(game_id, category_id)
                            game_category.save_to_db(cursor)
                    game.update(cursor)
                else:
                    return {'message': 'Game with id {id} not found'.format(id=game_id)}, 404
        except mysql.connector.Error as e:
            raise InternalServerError(e)
        except ValueError as e:
            raise BadRequestError()
        except Exception as e:
            raise InternalServerError(e)

        return {'message': 'Game edited successfully.'}, 201

class AddKey(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "game_id", type=int,  required=True, help="This field cannot be left blank!"        
    )
    parser.add_argument(
        "key", type=str,  required=True, help="This field cannot be left blank!"     
    )

    @classmethod
    @jwt_required
    @require_admin
    def post(cls):
        data = cls.parser.parse_args()  
        key_str = data['key']    
        game_id = data['game_id']
        
        try:
            with dbCursor() as cursor:
                game = GameModel.find_by_id(cursor,game_id)
                if game is None:
                    return {'message' : "Error when appending a key, game id not found"}, 404
                if game.is_digital == False:
                    return {'message' : "Error when appending a key, game of id {game_id} is not digital".format(game_id=game_id)}, 400
                key = KeyModel.find_by_key(cursor,game_id,key_str)
                if key:
                    return {'message' : "Error when appending a key, already in database", "key" : key.json()}, 409  

                key = KeyModel(game_id,key_str)                  
                key.save_to_db(cursor)

                return {'message': 'Key added sucessfully.'}, 201

        except Exception as e:
            raise InternalServerError(e)

        
class AddCategory(Resource):   
    
    @classmethod
    @jwt_required
    @require_admin
    def put(cls,name):
        try:
           
            with dbCursor() as cursor:
                category = CategoryModel.find_by_name(cursor,name)
                if category:
                    return {'message': "Error when appending a category {n}, already in database".format(n=name)}, 409
                else:                
                    category = CategoryModel(name)
                    category.save_to_db(cursor)
                
                return {'message': 'Category added sucessfully.'}, 201
                
        except Exception as e:
            raise InternalServerError(e)

class DeleteCategory(Resource):

    @classmethod
    @jwt_required
    @require_admin
    def delete(cls, name):
        try:

            with dbCursor() as cursor:
                category = CategoryModel.find_by_name(cursor, name)
                if category:
                    category = CategoryModel(name)
                    category.delete_from_db(cursor)
                else:
                    return {'message': "Error when deleting a category {n}, category doesnt exist".format(n=name)}, 404

                return {'message': 'Category deleted sucessfully.'}, 201

        except Exception as e:
            raise InternalServerError(e)


class AddPlatform(Resource):

    @classmethod
    @jwt_required
    @require_admin
    def put(cls, name):
        try:

            with dbCursor() as cursor:
                platform = PlatformModel.find_by_name(cursor, name)
                if platform:
                    return {'message': "Error when appending a platform {n}, already in database".format(n=name)}, 409
                else:
                    platform = PlatformModel(name)
                    platform.save_to_db(cursor)

                return {'message': 'Platform added sucessfully.'}, 201

        except Exception as e:
            raise InternalServerError(e)

class DeletePlatform(Resource):

    @classmethod
    @jwt_required
    @require_admin
    def delete(cls, name):
        try:

            with dbCursor() as cursor:
                platform = PlatformModel.find_by_name(cursor, name)
                if platform:
                    platform = PlatformModel(name)
                    platform.delete_from_db(cursor)
                else:
                    return {'message': "Error when deleting a platform {n}, platform doesnt exist".format(n=name)}, 404

                return {'message': 'Category deleted sucessfully.'}, 201

        except Exception as e:
            raise InternalServerError(e)


class FetchAllShoppings(Resource):

    @classmethod
    @jwt_required
    @require_admin
    def get(cls):
        try:
            with dbCursor() as cursor:
                all_user_transactions = UserTransactionModel.find_all(cursor)
                results = []
                for user_tr in all_user_transactions:
                    user = UserModel.find_by_id(cursor, user_tr.user_id).json()
                    res = []
                    game_transactions = GameTransactionModel.find_by_user_transaction_id(cursor, user_tr.id)
                    for game_tr in game_transactions:
                        res.append(game_tr.json_adv(cursor))
                    result = user_tr.json()
                    result['username'] = user['username']
                    result['games_transactions'] = res

                    results.append(result)

                return {"transactions": results}

        except Exception as e:
            raise InternalServerError(e)

class FetchAllUsers(Resource):

    @classmethod
    @jwt_required
    @require_admin
    def get(cls):
        try:
            with dbCursor() as cursor:
                all_users = UserModel.find_all(cursor)
                return {
                    'users' : [user.json() for user in all_users]
                }

        except Exception as e:
            raise InternalServerError(e)

class FetchGameKeys(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "game_id", type=int, required=True, help="This field cannot be left blank!"
    )
    @classmethod
    @jwt_required
    @require_admin
    def get(cls):
        data = cls.parser.parse_args()
        game_id = data['game_id']
        try:
            with dbCursor() as cursor:
                game = GameModel.find_by_id(cursor,game_id)
                if game:
                    keys = KeyModel.find_all_by_game_id(cursor, game_id)
                    return {
                        'keys' : [key.json() for key in keys]
                    }
                else:
                    return {'message': "Error, incorrect game id"}, 404

        except Exception as e:
            raise InternalServerError(e)