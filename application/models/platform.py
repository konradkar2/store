from __future__ import annotations
from datetime import datetime
from typing import List

class PlatformModel:
    def __init__(self,name: str, _id=None):
        self.name = name
        self.id = _id
    
    def json(self):
        return {
            "name": self.name,
            "id": self.id           
        }
    @classmethod
    def find_by_id(cls,cursor,_id: int) -> PlatformModel:
                
        query = "SELECT * FROM platforms WHERE id = %s"
        params = (_id,)
        cursor.execute(query, params)       
        platformData = cursor.fetchone()

        platform = None
        if(platformData):
            _id,name = platformData
            platform = PlatformModel(name,_id) 
            
        return platform
    @classmethod
    def find_by_name(cls,cursor,name: str) -> PlatformModel:                     
        query = "SELECT * FROM platforms WHERE name = %s"
        params = (name,)
        cursor.execute(query, params)
        platformData = cursor.fetchone()

        platform = None
        if(platformData):
            _id,name = platformData
            platform = PlatformModel(name,_id) 
            
        return platform
    @classmethod
    def find_all(cls,cursor) -> List[PlatformModel]:       
        query = "SELECT * FROM platforms"           
        cursor.execute(query)
        platformData = cursor.fetchall()
        
        platforms = []
        for row in platformData:
            _id,name = row
            platform = PlatformModel(name,_id)   
            platforms.append(platform)          
        
        return platforms    
    def save_to_db(self,cursor):             
        query = "INSERT INTO platforms (name) VALUES (%s)"
        params = (self.name,)
        cursor.execute(query, params)
        self.id = cursor.lastrowid

    def delete_from_db(self, cursor):
        query = "DELETE FROM platforms WHERE (name) = (%s)"
        params = (self.name,)
        cursor.execute(query, params)