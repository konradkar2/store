from __future__ import annotations
from datetime import datetime
from typing import List


class KeyModel():
    def __init__(self,game_id: int, key: str,used: bool = False, _id: int = None):
        self.id = _id
        self.game_id = game_id
        self.used = used
        self.key = key

    def json(self):
        return {
            "id": self.id,
            "game_id" : self.game_id,
            "used": self.used,
            "key": self.key
        }
   
    @classmethod 
    def get_quantity(cls,cursor,game_id: int) -> int:   
        quantity = 0     
         
        query = "SELECT count(*) FROM games_keys WHERE game_id = %s AND used = 0"
        params = (game_id,)
        cursor.execute(query, params)
        quantity = cursor.fetchone()           
        return quantity[0]
       
    @classmethod
    def find_by_key(cls,cursor,game_id: int, key: str):        
        query = "SELECT * FROM games_keys WHERE game_id = %s AND gkey = %s"
        params = (game_id,key)
        cursor.execute(query, params)
        keyData = cursor.fetchone()
        
        key = None
        if keyData:
            _id,game_id,used,key = keyData
            key = KeyModel(game_id,key,used,_id)
        return key
    @classmethod
    def find_by_id(cls,cursor,_id):        
        query = "SELECT * FROM games_keys WHERE id = %s"
        params = (_id,)
        cursor.execute(query, params)
        keyData = cursor.fetchone()
        
        key = None
        if keyData:
            _id,game_id,used,key = keyData
            key = KeyModel(game_id,key,used,_id)
        return key

    @classmethod
    def find_any_not_used(cls,cursor,game_id: int):        
        query = "SELECT * FROM games_keys WHERE game_id = %s AND used = 0"
        params = (game_id,)
        cursor.execute(query, params)
        keyData = cursor.fetchone()
        
        key = None
        if keyData:
            _id,game_id,used,key = keyData
            key = KeyModel(game_id,key,used,_id)
        return key
    
    def save_to_db(self,cursor):         
        query = "INSERT INTO games_keys (game_id, used, gkey) VALUES (%s, %s,%s)"
        params = (self.game_id,self.used,self.key)
        cursor.execute(query, params)
        self.id = cursor.lastrowid
        

