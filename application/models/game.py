from __future__ import annotations
from datetime import datetime
from typing import List
from store.application.models.game_category import GameCategoryModel
from store.application.models.platform import PlatformModel
from store.application.models.key import KeyModel
#todo:verify email 
#change "name" to "username" in database
class GameModel():
    def __init__(self,name: str,price: float,
             quantity: int, description: str, 
             release_date: str, is_digital: bool,
             platform_id: int,age_category: str , _id: int = None):
        
        self.name = name
        self.price = price
        self.quantity = quantity
        self.description = description
        self.release_date = release_date
        self.is_digital = is_digital       
        self.platform_id = platform_id
        self.age_category = age_category
        
        self.id = _id
        
    def json(self,cursor):   
        platform = PlatformModel.find_by_id(cursor,self.platform_id) 
        print(platform)
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": float(self.price),
            "quantity": self.get_quantity(cursor),
            "is_digital" : self.is_digital,
            "age_category": self.age_category,
            "platform" : platform.json(),
            "categories" : [category.json(cursor) for category in GameCategoryModel.find_many_by_game_id(cursor,self.id)]     
        }
    
    def get_quantity(self,cursor) -> int:
        if self.is_digital:
            return KeyModel.get_quantity(cursor,self.id)
        else:
            return self.quantity
    
    @classmethod
    def find_by_id(cls,cursor,_id: int) -> GameModel:       
        query = "SELECT * FROM games WHERE id = %s"
        params = (_id,)
        cursor.execute(query, params)
        gameData = cursor.fetchone()

        game = None
        if(gameData):
            _id,name,price,quantity,description,release_date,is_digital,age_category,platform_id = gameData
            game = GameModel(name,price,quantity,description,release_date,is_digital,platform_id,age_category,_id)       
            
        return game
    @classmethod
    def find_many_by_filter(cls,cursor,number_per_page,page_number: int,name: str,categories_id: List[str],
                    platforms_id: List[str],order_by: str,order_rule: str):
        
        limit = number_per_page
        offset  = (page_number -1 ) * number_per_page

        if order_by is None:
            order_by = 'name'
        if order_rule is None:
            order_rule = 'ASC'
        if order_by not in ('price','name') or order_rule not in ('ASC,DESC,asc,desc'):
            raise Exception        
            
        if platforms_id:
            platforms_format = ','.join(['%s'] * len(platforms_id))         
        if categories_id:
            categories_format = ','.join(['%s'] * len(categories_id))
        #create query
        query = "SELECT SQL_CALC_FOUND_ROWS * FROM games g\n"          
        query += "WHERE g.name LIKE %s\n"

        if platforms_id:
            query += "AND g.platform_id IN (%s)\n" % platforms_format            
        if categories_id:
            query += "AND g.id in (select gc.game_id from games_categories gc where gc.game_id = g.id and gc.category_id in (%s))\n" % categories_format       
        
        query += "ORDER BY {c} {r}\n".format(c=order_by,r=order_rule)       
        query += "LIMIT {lim} OFFSET {off}\n".format(lim=limit,off=offset)      
        params = []
        #create proper params
        if name:
            params.append('%' + name + '%')
        else:
            params.append("%%")
        if platforms_id:
            for p in platforms_id:
                params.append(p)
        if categories_id: 
            for c in categories_id:
                params.append(c)          
             
        params = tuple(params)       
        cursor.execute(query, params)                   
        gameData = cursor.fetchall()

        games = []
        for row in gameData:          
            _id,name,price,quantity,description,release_date,is_digital,age_category,platform_id = row
            game = GameModel(name,price,quantity,description,release_date,is_digital,platform_id,age_category,_id)  
            games.append(game)

        return games
        

    @classmethod
    def find_many_by_name(cls,cursor,name: str) -> List[GameModel]:      
        query = "SELECT * FROM games WHERE name LIKE %s"
        params = (name + "%",)
        cursor.execute(query, params)
        gameData = cursor.fetchall()
            
        games = []
        for row in gameData:          
            _id,name,price,quantity,description,release_date,is_digital,platform_id,age_category = row
            game = GameModel(name,price,quantity,description,release_date,is_digital,platform_id,age_category,_id)  
            games.append(game)

        return games
         
    def save_to_db(self,cursor):        
        query = "INSERT INTO games (name,price,quantity,description,release_date,is_digital,platform_id,age_category) VALUES (%s, %s,%s,%s,%s, %s,%s,%s)"
        params = (self.name,self.price,self.quantity,self.description,self.release_date,self.is_digital,self.platform_id,self.age_category)
        cursor.execute(query, params)
        self.id = cursor.lastrowid
