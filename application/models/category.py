from __future__ import annotations
from datetime import datetime
from typing import List




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
    def find_by_id(cls,cursor,_id: int) -> CategoryModel:                   
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
    def find_by_name(cls,cursor,name: str) -> CategoryModel:                 
        query = "SELECT * FROM categories WHERE name = %s"
        params = (name,)
        cursor.execute(query, params)
        categoryData = cursor.fetchone()

        category = None
        if(categoryData):
            _id,name = categoryData
            category = CategoryModel(name,_id) 
            
        return category
    @classmethod
    def find_all(cls,cursor) -> List[CategoryModel]:         
        query = "SELECT * FROM categories"            
        cursor.execute(query)
        categoryData = cursor.fetchall()
        
        categories = []
        for row in categoryData:
            _id,name = row
            category = CategoryModel(name,_id)   
            categories.append(category)          
        
        return categories    
    def save_to_db(self,cursor):         
        query = "INSERT INTO categories (name) VALUES (%s)"
        params = (self.name,)
        cursor.execute(query, params)
        self.id = cursor.lastrowid

    def delete_from_db(self, cursor):
        query = "DELETE FROM categories WHERE (name) = (%s)"
        params = (self.name,)
        cursor.execute(query, params)


