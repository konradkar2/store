from __future__ import annotations
from store.application.utils.db import dbReadCursor,dbTransactionCursor
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
    def find_by_key(cls,game_id: int, key: str):
        with dbReadCursor() as cursor:  
            query = "SELECT * FROM mydb.keys WHERE keys.game_id = %s AND keys.key = %s"
            params = (game_id,key)
            cursor.execute(query, params)
            keyData = cursor.fetchone()
        
        key = None
        if keyData:
            _id,game_id,used,key = keyData
            key = KeyModel(game_id,key,used,_id)
        return key

    @classmethod
    def find_any_not_used(cls,game_id: int):
        pass
    
    def save_to_db(self):
        with dbTransactionCursor(self) as cursor:        
            query = "INSERT INTO mydb.keys (keys.game_id, keys.used, keys.key) VALUES (%s, %s,%s)"
            params = (self.game_id,self.used,self.key)
            cursor.execute(query, params)

        

