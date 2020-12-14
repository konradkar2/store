from app import get_db
#todo:verify email 

class UserModel():
    def __init__(self,name: str,email: str,password_hash: str,salt: str):
        
        self.name = name
        self.password_hash = password_hash
        self.salt = salt
        self.email = email
        
    def json(self):
        return {
            "username": self.username,
            "id": self.id,
            "email" : self.email
        }
    @classmethod
    def find_by_username(cls,username):
        pass            
    
    def save_to_db(self):
        mydb = get_db()
        cursor = mydb.cursor()
        
        query = "INSERT INTO users (name, email, password_hash, salt) VALUES (%s, %s,%s,%s)"
        params = (self.name,self,email,self.password_hash,self.salt)
        cursor.execute(query, params)

        mydb.commit()


user = UserModel("test1","test1@gmail.com","aaaaaaaaaaaa","bbbbbbbbbbbb")

user.save_to_db()