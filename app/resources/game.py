from flask_restful import Resource, reqparse
from models.game import GameModel
import mysql.connector
from exceptions import InternalServerError, BadRequestError
from flask_jwt_extended import create_access_token

from datetime import datetime

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
        "category_id", type=int, required=True, help="This field cannot be left blank!"
    )
    parser.add_argument(
        "platform_id", type=int, required=True, help="This field cannot be left blank!"
    )
    parser.add_argument(
        "age_category", type=str,  required=True, help="This field cannot be left blank!"
    )

    @classmethod
    def post(cls):
        data = cls.parser.parse_args()
  
        try:
            now = datetime.utcnow()
            data['release_date'] = now.strftime('%Y-%m-%d %H:%M:%S')

            game = GameModel(**data)
            game.save_to_db()
        except mysql.connector.Error as e:
            raise InternalServerError(e)
        except ValueError as e:
            raise BadRequestError()
        except Exception as e:
            raise InternalServerError(e)

        return {'message': 'Game added successfully.'}, 201