from __future__ import annotations
from store.application.utils.db import dbReadCursor,dbTransactionCursor


class GameTransactionModel():
    def __init__(self,user_transaction_id: int,game_id: int, key_id: int, _id = None):
        self.id = _id
        self.user_transaction_id = user_transaction_id
        self.game_id = game_id
        self.key_id = key_id
       

    def json(self):
        return {
            "id": self.id,
            "user_transaction_id": self.user_transaction_id,
            "game_id" : self.game_id,
            "key_id" : self.key_id
        }

    @classmethod
    def find_by_id(cls,_id):
        with dbReadCursor() as cursor:  
            query = "SELECT * FROM users_transactions WHERE id = %s"
            params = (_id,)
            cursor.execute(query, params)
            transactionData = cursor.fetchone()
        
        gameTransaction = None
        if transactionData:
            _id,user_transaction_id,game_id,key_id = transactionData
            gameTransaction = GameTransactionModel(user_transaction_id,game_id,key_id,_id)
        return gameTransaction

    @classmethod
    def find_by_user_transaction_id(cls,user_transaction_id: int):
        with dbReadCursor() as cursor:  
            query = "SELECT * FROM games_transactions WHERE user_transaction_id = %s"
            params = (user_transaction_id_id,)
            cursor.execute(query, params)
            gameTransactionsData = cursor.fetchall()
        
        gameTransactions = []
        for gtData in gameTransactionsData:
            _id,user_transaction_id,game_id,key_id = gtData
            gtr = GameTransactionModel(user_transaction_id,game_id,key_id,_id)
            gameTransactions.append(gtr)
        
        return gameTransactions
    
    def save_to_db(self):
        with dbTransactionCursor(self) as cursor:        
            query = "INSERT INTO games_transactions (user_transaction_id,game_id,key_id) VALUES (%s, %s,%s)"
            params = (self.user_transaction_id,self.game_id,self.key_id)
            cursor.execute(query, params)
