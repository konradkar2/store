from __future__ import annotations
from datetime import datetime
from typing import List

from store.application.utils.db import get_db,dbTransactionCursor


class CategoryModel:
    def __init__(self,name: str, game_id: int, _id=None):
        self.name = name
        self.game_id = game_id
        self.id = _id
    
    def json(self):
        return {
            "name": self.name,
            "game_id": self.game_id,               
        }
    @classmethod
    def find_by_id(cls,_id: int) -> CategoryModel:
        mydb = get_db()
        cursor = mydb.cursor()
        
        query = "SELECT * FROM categories WHERE id = %s"
        params = (_id,)
        cursor.execute(query, params)

        categoryData = cursor.fetchone()
        category = None
        if(categoryData):
            _id,name,game_id = categoryData
            category = CategoryModel(name,game_id,_id) 
            
        return category
    @classmethod
    def find_many_by_game_id(cls,game_id: int) -> List[CategoryModel]:
        mydb = get_db()
        cursor = mydb.cursor()
        
        query = "SELECT * FROM categories WHERE game_id = %s"
        params = (game_id,)
        cursor.execute(query, params)

        categoryData = cursor.fetchall()
        
        categories = []
        for row in categoryData:
            _id,name,game_id = row
            category = CategoryModel(name,game_id,_id)   
            categories.append(category)          
        
        return categories    
    def save_to_db(self):
        with dbTransactionCursor(self) as cursor:        
            query = "INSERT INTO categories (name,game_id) VALUES (%s, %s)"
            params = (self.name,self.game_id)
            cursor.execute(query, params)