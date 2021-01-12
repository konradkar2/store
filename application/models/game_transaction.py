from __future__ import annotations

from store.application.models.game import GameModel
from store.application.models.key import KeyModel


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
    def json_adv(self,cursor):
        game = GameModel.find_by_id(cursor,self.game_id)
        key = None
        if game.is_digital:
            key = KeyModel.find_by_id(cursor,self.key_id).key
        return {
            "id" : self.id,
            "user_transaction_id": self.user_transaction_id,
            "game_id" : self.game_id,
            "game_name" : game.name,
            "key_id" : self.key_id,
            "key": key
        }

    @classmethod
    def find_by_id(cls,cursor,_id):        
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
    def find_by_user_transaction_id(cls,cursor,user_transaction_id: int):       
        query = "SELECT * FROM games_transactions WHERE user_transaction_id = %s"
        params = (user_transaction_id,)
        cursor.execute(query, params)
        gameTransactionsData = cursor.fetchall()
        
        gameTransactions = []
        for gtData in gameTransactionsData:
            _id,user_transaction_id,game_id,key_id = gtData
            gtr = GameTransactionModel(user_transaction_id,game_id,key_id,_id)
            gameTransactions.append(gtr)
        
        return gameTransactions
    
    def save_to_db(self,cursor):        
        query = "INSERT INTO games_transactions (user_transaction_id,game_id,key_id) VALUES (%s, %s,%s)"
        params = (self.user_transaction_id,self.game_id,self.key_id)
        cursor.execute(query, params)
        print(cursor.statement)
        self.id = cursor.lastrowid

