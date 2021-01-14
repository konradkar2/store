from flask_restful import Resource, reqparse
import mysql.connector
from flask_jwt_extended import create_access_token,jwt_required,get_jwt_identity
from store.application.resources.authorize import require_admin

from store.application.exceptions import InternalServerError
from store.application.models.user import UserModel
from store.application.utils.security import encrypt_base64, verifyHash_base64
from store.application.utils.db import dbCursor

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
        try: 
            with dbCursor() as cursor:
                if UserModel.find_by_username(cursor, data["username"]):
                    return {"message": "User already exists"}, 409
                if UserModel.find_by_email(cursor, data["email"]):
                    return {"message": "This email is already taken"}, 409
                
                password_hash, salt = encrypt_base64(data['password'])            
                role = 'user'
                user = UserModel(data['username'],data['email'],role,password_hash,salt)
                user.save_to_db(cursor)
        except mysql.connector.Error as e:
            raise InternalServerError(e)
        except Exception as e:
            raise InternalServerError(e)

        return {'message': 'User created successfully.'}, 201

class AdminRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "username", type=str, required=True, help="This field cannot be left blank!"
    )
    parser.add_argument(
        "password", type=str, required=True, help="This field cannot be left blank!"
    )
    parser.add_argument(
        "email", type=str, required=True, help="This field cannot be left blank!"
    )

    @classmethod
    @jwt_required
    @require_admin
    def post(cls):
        data = cls.parser.parse_args()
        try:
            with dbCursor() as cursor:
                if UserModel.find_by_username(cursor, data["username"]):
                    return {"message": "User already exists"}, 409
                if UserModel.find_by_email(cursor, data["email"]):
                    return {"message": "This email is already taken"}, 409

                password_hash, salt = encrypt_base64(data['password'])
                role = 'admin'
                user = UserModel(data['username'], data['email'], role, password_hash, salt)
                user.save_to_db(cursor)
        except mysql.connector.Error as e:
            raise InternalServerError(e)
        except Exception as e:
            raise InternalServerError(e)

        return {'message': 'Admin created successfully.'}, 201
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
            with dbCursor() as cursor:
                user = UserModel.find_by_username(cursor,data['username'])
                if user is None:
                    return {'message' : "Invalid credentials"}, 401   
            
            result = verifyHash_base64(data['password'],user.password_hash,user.salt)                       

            if result:
                claims = {'role' : user.role}
                access_token = create_access_token(identity=user.id,user_claims=claims,fresh=True,expires_delta=False)
                #refresh_token = create_refresh_token(user.id)
                return {
                    'access_token': access_token,                    
                    'user': user.json()
                },200
            return {'message' : "Invalid credentials"}, 401   
        except mysql.connector.Error as e:
            raise InternalServerError(e)
        except Exception as e:
            raise InternalServerError(e)

class ChangePassword(Resource):    
    parser = reqparse.RequestParser()
    parser.add_argument(
        "oldpass", type=str, required=True, help="This field cannot be left blank!"
    )
    parser.add_argument(
        "newpass", type=str, required=True, help="This field cannot be left blank!"
    )
    @classmethod
    @jwt_required
    def put(cls):
        data = cls.parser.parse_args()
        try:
            with dbCursor() as cursor:
                user_id = get_jwt_identity()
                user = UserModel.find_by_id(cursor,user_id)                
                result = verifyHash_base64(data['oldpass'],user.password_hash,user.salt)                       
                if not result:
                    return {"message": "Error when changing password, invalid credientials"}, 401
                    
                if result:
                    password_hash, salt = encrypt_base64(data['newpass'])
                    user.password_hash = password_hash
                    user.salt = salt

                    user.update(cursor)
                return {"message": "Password changed succesfully"}, 200
        except Exception as e:
            raise InternalServerError(e)

class ChangeEmail(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "newemail", type=str, required=True, help="This field cannot be left blank!"
    )

    @classmethod
    @jwt_required
    def put(cls):
        data = cls.parser.parse_args()
        try:
            with dbCursor() as cursor:
                new_email = data['newemail']
                user_id = get_jwt_identity()
                user = UserModel.find_by_id(cursor, user_id)

                if user:
                    user.email = new_email
                    user.update(cursor)
                return {"message": "Email changed succesfully"}, 200
        except Exception as e:
            raise InternalServerError(e)

class ChangeRole(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "newrole", type=str, required=True, help="This field cannot be left blank!"
    )
    parser.add_argument(
        "user_id", type=int, required=True, help="This field cannot be left blank!"
    )

    @classmethod
    @jwt_required
    @require_admin
    def put(cls):
        data = cls.parser.parse_args()
        try:
            with dbCursor() as cursor:
                new_role = data['newrole']
                user_id = data['user_id']
                user = UserModel.find_by_id(cursor, user_id)

                if user:
                    user.role = new_role
                    user.update(cursor)
                return {"message": "Role changed succesfully"}, 200
        except Exception as e:
            raise InternalServerError(e)

