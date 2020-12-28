from __future__ import annotations
from datetime import datetime
from typing import List

from store.application.utils.db import dbReadCursor,dbTransactionCursor
from store.application.models.game_category import GameCategoryModel
from store.application.models.key import KeyModel
#todo:verify email 
#change "name" to "username" in database
class GameModel():
    def __init__(self,name: str,price: float,
             quantity: int, description: str, 
             release_date: str, is_digital: bool,
             platform_id: int,age_category: str , _id: int = None):
        
        self.name = name
        self.price = price
        self.quantity = quantity
        self.description = description
        self.release_date = release_date
        self.is_digital = is_digital       
        self.platform_id = platform_id
        self.age_category = age_category
        
        self.id = _id
        
    def json(self):       
        return {
            "id": self.id,
            "name": self.name,
            "price": float(self.price),
            "quantity": self.quantity,
            "is_digital" : self.is_digital,
            "age_category": self.age_category,
            "categories" : [category.jsonMin() for category in GameCategoryModel.find_many_by_game_id(self.id)]  
        }
    
    def get_quantity(self) -> int:
        if self.is_digital:
            return KeyModel.get_quantity(self.id)
        else:
            return self.quantity
    
    @classmethod
    def find_by_id(cls,_id: int) -> GameModel:
        with dbReadCursor() as cursor:
            query = "SELECT * FROM games WHERE id = %s"
            params = (_id,)
            cursor.execute(query, params)
            gameData = cursor.fetchone()

        game = None
        if(gameData):
            _id,name,price,quantity,description,release_date,is_digital,platform_id,age_category = gameData
            game = GameModel(name,price,quantity,description,release_date,is_digital,platform_id,age_category,_id)       
            
        return game
    @classmethod
    def find_many_by_name(cls,name: str) -> List[GameModel]:
        with dbReadCursor() as cursor:
            query = "SELECT * FROM games WHERE name LIKE %s"
            params = (name + "%",)
            cursor.execute(query, params)
            gameData = cursor.fetchall()
            
        games = []
        for row in gameData:          
            _id,name,price,quantity,description,release_date,is_digital,platform_id,age_category = row
            game = GameModel(name,price,quantity,description,release_date,is_digital,platform_id,age_category,_id)  
            games.append(game)

        return games
         
    def save_to_db(self):
        with dbTransactionCursor(self) as cursor:        
            query = "INSERT INTO games (name,price,quantity,description,release_date,is_digital,platform_id,age_category) VALUES (%s, %s,%s,%s,%s, %s,%s,%s)"
            params = (self.name,self.price,self.quantity,self.description,self.release_date,self.is_digital,self.platform_id,self.age_category)
            cursor.execute(query, params)

