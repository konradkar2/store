from __future__ import annotations
from store.application.utils.db import dbReadCursor,dbTransactionCursor
from datetime import datetime


class TransactionModel():
    def __init__(self,user_id: int,date: str, _id = None):
        self.id = _id
        self.user_id = user_id
        self.date = date
       

    def json(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "date" : self.date,            
        }

    @classmethod
    def find_by_id(cls,_id):
        with dbReadCursor() as cursor:  
            query = "SELECT * FROM transactions WHERE id = %s"
            params = (_id,)
            cursor.execute(query, params)
            transactionData = cursor.fetchone()
        
        transaction = None
        if transactionData:
            _id,user_id,date = transactionData
            transaction = TransactionModel(user_id,date,_id)
        return transaction

    @classmethod
    def find_by_user_id(cls,user_id: int):
        with dbReadCursor() as cursor:  
            query = "SELECT * FROM transactions WHERE user_id = %s"
            params = (user_id,)
            cursor.execute(query, params)
            transactionsData = cursor.fetchall()
        
        transactions = []
        for tData in transactionsData:
            _id,user_id,date = tData
            tr = TransactionModel(user_id,date,_id)
            transactions.append(tr)
        
        return transactions
    
    def save_to_db(self):
        with dbTransactionCursor(self) as cursor:        
            query = "INSERT INTO transactions (user_id,date) VALUES (%s, %s)"
            params = (self.user_id,self.date)
            cursor.execute(query, params)