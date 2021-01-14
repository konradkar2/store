from __future__ import annotations


#todo:verify email 
#change "name" to "username" in database
class UserModel():
    def __init__(self,username: str,email: str, role: str,password_hash: str,salt: str, _id: str = None):
        
        self.username = username
        self.password_hash = password_hash
        self.salt = salt
        self.email = email
        self.role = role

        self.id = _id
        
    def json(self):
        return {
            "username": self.username,
            "id": self.id,
            "email" : self.email,
            "role" : self.role            
        }

    @classmethod
    def find_by_id(cls,cursor,_id: int) -> UserModel:                
        query = "SELECT * FROM users WHERE id = %s"
        params = (_id,)
        cursor.execute(query, params)
        userData = cursor.fetchone()
    
        user = None
        if(userData):
            _id,username,email,role,_hash,salt = userData
            user = UserModel(username,email,role,_hash,salt,_id)       
            
        return user

    @classmethod
    def find_by_username(cls,cursor,username: str) -> UserModel:                
        query = "SELECT * FROM users WHERE name = %s"
        params = (username,)
        cursor.execute(query, params)
        userData = cursor.fetchone()
    
        user = None
        if(userData):
            _id,username,email,role,_hash,salt = userData
            user = UserModel(username,email,role,_hash,salt,_id)       
            
        return user
    @classmethod
    def find_by_email(cls,cursor,email: str) -> UserModel:       
        query = "SELECT * FROM users WHERE email = %s"
        params = (email,)
        cursor.execute(query, params)
        userData = cursor.fetchone()
        
        user = None
        if(userData):
            _id,username,email,role,_hash,salt = userData
            user = UserModel(username,email,role,_hash,salt,_id)
            
        return user

    def save_to_db(self,cursor):              
        query = "INSERT INTO users (name, email,role, password_hash, salt) VALUES (%s, %s,%s,%s,%s)"
        params = (self.username,self.email,self.role,self.password_hash,self.salt)
        cursor.execute(query, params)
        self.id = cursor.lastrowid
    
    def update(self,cursor):
        query = "UPDATE users\n"
        query += "SET email=%s, password_hash=%s, salt=%s"
        query += "WHERE id=%s"
        params = (self.email,self.password_hash,self.salt,self.id)
        cursor.execute(query,params)

        
        
        

       

        


