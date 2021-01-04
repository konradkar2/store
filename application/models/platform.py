from __future__ import annotations
from datetime import datetime
from typing import List

from store.application.utils.db import dbReadCursor,dbTransactionCursor


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
    def find_by_id(cls,_id: int) -> PlatformModel:
        with dbReadCursor() as cursor:              
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
    def find_by_name(cls,name: str) -> PlatformModel:
        with dbReadCursor() as cursor:              
            query = "SELECT * FROM platforms WHERE name = %s"
            params = (_id,)
            cursor.execute(query, params)
            platformData = cursor.fetchone()

        platform = None
        if(platformData):
            _id,name = platformData
            platform = PlatformModel(name,_id) 
            
        return platform
    @classmethod
    def find_all(cls,) -> List[PlatformModel]:
        with dbReadCursor() as cursor:    
            query = "SELECT * FROM platforms"           
            cursor.execute(query)
            platformData = cursor.fetchall()
        
        platforms = []
        for row in platformData:
            _id,name = row
            platform = PlatformModel(name,_id)   
            platforms.append(platform)          
        
        return platforms    
    def save_to_db(self):
        with dbTransactionCursor(self) as cursor:        
            query = "INSERT INTO platforms (name) VALUES (%s)"
            params = (self.name,)
            cursor.execute(query, params)