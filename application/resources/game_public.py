from flask_restful import Resource, reqparse
import mysql.connector
from flask_jwt_extended import jwt_required,get_jwt_identity
from datetime import datetime

from store.application.models.game import GameModel
from store.application.exceptions import InternalServerError, BadRequestError



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
