from flask_restful import Resource, reqparse
from models.user import UserModel
from utils.security import encrypt_base64, verifyHash_base64
import mysql.connector
from exceptions import InternalServerError

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "username", type=str, required=True, help="This field cannot be left blank!"
    )
    parser.add_argument(
        "password", type=str, required=True, help="This field cannot be left blank!"
    )
    parser.add_argument(
        "email", type=str,  required=True, help="This field cannot be left blank!"
    )
    @classmethod
    def post(cls):
        data = cls.parser.parse_args()

        if UserModel.find_by_username(data["username"]):
            return {"message": "User already exists"}, 400
        try:
            password_hash, salt = encrypt_base64(data['password'])
            print(len(password_hash))

            user = UserModel(data['username'],data['email'],password_hash,salt)
            user.save_to_db()
        except mysql.connector.Error as err:
            raise InternalServerError(err)

        return {'message': 'User created successfully.'}, 201