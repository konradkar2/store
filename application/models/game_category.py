from __future__ import annotations
from datetime import datetime
from typing import List

from store.application.models.category import CategoryModel

class GameCategoryModel:
    def __init__(self, game_id: int,category_id: int, _id=None):       
        self.game_id = game_id
        self.category_id = category_id
        self.id = _id
    
    def json(self,cursor):
        category = CategoryModel.find_by_id(cursor,self.category_id)       
        return {                      
            "category_id" : self.category_id,
            "category_name": category.name          
        }
    def jsonMin(self):        
        return {            
            "game_id": self.game_id,    
            "category_id" : self.category_id                       
        }
    @classmethod
    def find_by_id(cls,cursor,_id: int) -> GameCategoryModel:                    
        query = "SELECT * FROM games_categories WHERE id = %s"
        params = (_id,)
        cursor.execute(query, params)
        categoryData = cursor.fetchone()

        category = None
        if(categoryData):
            _id,name,game_id = categoryData
            category = GameCategoryModel(name,game_id,_id) 
            
        return category
    @classmethod
    def find_many_by_game_id(cls,cursor,game_id: int) -> List[GameCategoryModel]:
        query = "SELECT * FROM games_categories WHERE game_id = %s"
        params = (game_id,)
        cursor.execute(query, params)
        categoryData = cursor.fetchall()
        
        games_categories = []
        for row in categoryData:
            _id,name,game_id = row
            category = GameCategoryModel(name,game_id,_id)   
            games_categories.append(category)          
        
        return games_categories

    @classmethod
    def delete_by_game_id(cls, cursor, game_id):
        query = "DELETE FROM games_categories WHERE game_id = %s"
        params = (game_id,)
        cursor.execute(query, params)
        cursor.id = cursor.lastrowid

    def save_to_db(self,cursor):        
        query = "INSERT INTO games_categories (game_id,category_id) VALUES (%s, %s)"
        params = (self.game_id,self.category_id)
        cursor.execute(query, params)
        self.id = cursor.lastrowid