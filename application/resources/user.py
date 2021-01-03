from flask_restful import Resource, reqparse
import mysql.connector
from flask_jwt_extended import create_access_token

from store.application.exceptions import InternalServerError
from store.application.models.user import UserModel
from store.application.utils.security import encrypt_base64, verifyHash_base64


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

        if len(data["username"]) < 6:
            return {"message": "Username too short"}, 400
        if len(data["password"]) < 6:
            return {"message": "Password too short"}, 400

        if UserModel.find_by_username(data["username"]):
            return {"message": "User already exists"}, 400
        if UserModel.find_by_email(data["email"]):
            return {"message": "This email is already taken"}, 400

        try:
            password_hash, salt = encrypt_base64(data['password'])            
            role = 'user'
            user = UserModel(data['username'],data['email'],role,password_hash,salt)
            user.save_to_db()
        except mysql.connector.Error as e:
            raise InternalServerError(e)
        except Exception as e:
            raise InternalServerError(e)

        return {'message': 'User created successfully.'}, 201

class UserLogin(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "username", type=str, required=True, help="This field cannot be left blank!"
    )
    parser.add_argument(
        "password", type=str, required=True, help="This field cannot be left blank!"
    )
    
    @classmethod
    def post(cls):
        data = cls.parser.parse_args()
        try:
            user = UserModel.find_by_username(data['username'])
            if user is None:
                return {'message' : "Invalid credentials"}, 401   
            
            result = verifyHash_base64(data['password'],user.password_hash,user.salt)                       

            if result:
                claims = {'role' : user.role}
                access_token = create_access_token(identity=user.id,user_claims=claims,fresh=True)
                #refresh_token = create_refresh_token(user.id)
                return {
                    'access_token': access_token,
                    'role' : user.role,
                    'user': user.json()
                },200
            return {'message' : "Invalid credentials"}, 401   
        except mysql.connector.Error as e:
            raise InternalServerError(e)
        except Exception as e:
            raise InternalServerError(e)