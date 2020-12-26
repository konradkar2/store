from __future__ import annotations
from store.application.utils.db import get_db,dbTransactionCursor
from datetime import datetime
from typing import List


class KeyModel():
    def __init__(self,game_id: int, key: str,used: bool = False, _id: int = None):
        self.id = _id
        self.game_id = game_id,
        self.used = used,
        self.key = key
    
    def save_to_db(self):
        with dbTransactionCursor(self) as cursor:        
            query = "INSERT INTO keys (game_id,used,key) VALUES (%s, %s,%s)"
            params = (self.game_id,self.used,self.key)
            cursor.execute(query, params)

        

