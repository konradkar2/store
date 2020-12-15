from __future__ import annotations
from utils.db import get_db

#todo:verify email 
#change "name" to "username" in database
class UserModel():
    def __init__(self,username: str,email: str,password_hash: str,salt: str, _id: str = None):
        
        self.username = username
        self.password_hash = password_hash
        self.salt = salt
        self.email = email
        
        self.id = _id
        
    def json(self):
        return {
            "username": self.username,
            "id": self.id,
            "email" : self.email
        }
    @classmethod
    def find_by_username(cls,username: str) -> UserModel:
        mydb = get_db()
        cursor = mydb.cursor()
        
        query = "SELECT * FROM users WHERE name = %s"
        params = (username,)
        cursor.execute(query, params)

        userData = cursor.fetchone()
        user = None
        if(userData):
            _id,username,_hash,salt,email = userData
            user = UserModel(username,email,_hash,salt,_id)       
            
        return user
    @classmethod
    def find_by_email(cls,email: str) -> UserModel:
        mydb = get_db()
        cursor = mydb.cursor()
        
        query = "SELECT * FROM users WHERE email = %s"
        params = (email,)
        cursor.execute(query, params)

        userData = cursor.fetchone()
        user = None
        if(userData):
            _id,username,_hash,salt,email = userData
            user = UserModel(username,email,_hash,salt,_id)       
            
        return user
    
    def save_to_db(self):
        mydb = get_db()
        cursor = mydb.cursor()
        
        query = "INSERT INTO users (name, email, password_hash, salt) VALUES (%s, %s,%s,%s)"
        params = (self.username,self.email,self.password_hash,self.salt)
        cursor.execute(query, params)

        mydb.commit()


