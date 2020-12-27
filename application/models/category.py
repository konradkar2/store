from __future__ import annotations
from datetime import datetime
from typing import List

from store.application.utils.db import dbReadCursor,dbTransactionCursor


class CategoryModel:
    def __init__(self,name: str, _id=None):
        self.name = name
        self.id = _id
    
    def json(self):
        return {
            "name": self.name,
            "id": self.id           
        }
    @classmethod
    def find_by_id(cls,_id: int) -> CategoryModel:
        with dbReadCursor() as cursor:              
            query = "SELECT * FROM categories WHERE id = %s"
            params = (_id,)
            cursor.execute(query, params)
            categoryData = cursor.fetchone()

        category = None
        if(categoryData):
            _id,name = categoryData
            category = CategoryModel(name,_id) 
            
        return category
    @classmethod
    def find_by_name(cls,name: str) -> CategoryModel:
        with dbReadCursor() as cursor:              
            query = "SELECT * FROM categories WHERE name = %s"
            params = (_id,)
            cursor.execute(query, params)
            categoryData = cursor.fetchone()

        category = None
        if(categoryData):
            _id,name = categoryData
            category = CategoryModel(name,_id) 
            
        return category
    @classmethod
    def find_all(cls,game_id: int) -> List[CategoryModel]:
        with dbReadCursor() as cursor:    
            query = "SELECT * FROM categories"
            params = (game_id,)
            cursor.execute(query, params)
            categoryData = cursor.fetchall()
        
        categories = []
        for row in categoryData:
            _id,name = row
            category = CategoryModel(name,_id)   
            categories.append(category)          
        
        return categories    
    def save_to_db(self):
        with dbTransactionCursor(self) as cursor:        
            query = "INSERT INTO categories (name) VALUES (%s)"
            params = (self.name,)
            cursor.execute(query, params)