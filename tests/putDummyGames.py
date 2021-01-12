from flask import Flask
import unittest
from flask_testing import TestCase
import json

from store.application import app
from store.tests.utils import print_test_time_elapsed, get_random_string, get_token_from_response
from store.application.models.user import UserModel
from store.application.models.category import CategoryModel
from store.application.models.platform import PlatformModel
from store.application.models.game import GameModel
from store.application.resources.user import UserLogin
from store.application.resources.game_admin import AddGame, AddKey
from store.application.utils.security import encrypt_base64, verifyHash_base64
from store.tests.putDummyData import resetDb

import csv
import random

class PutGames(TestCase):
    def setUp(self):
        print(app)
        self.client = app.app.test_client()

    def tearDown(self):
        pass

    def create_app(self):
        """
        This is a requirement for Flask-Testing
        """
        app = Flask(__name__)
        app.config['TESTING'] = True

        return app

    @print_test_time_elapsed
    def test_gamemodel(self):      
        username = "admin1"        
        password = "admin1"      
       
        post_data = {'username' : username, 'password' : password}
        login = self.client.post('/auth', data=post_data)            
        token = login.data.decode('utf8')
        token = json.loads(token)
        token_admin = token['access_token']      
        
        i = 0

        

        #add categories
        with open('store/tests/games.csv', newline='',encoding='utf-8') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',')
            for row in spamreader:
                if i==0:
                    i = i + 1
                    continue
                name = row[0]
                description = row[1]
                price = row[2]
                platform = row[3]
                categories = row[4]
                is_digital = row[5]
                quantity = row[6]
                
                cat = categories.split(',')
                for c in cat:
                    c = c.lower()
                    post_headers_user = {'Authorization': 'Bearer ' +token_admin }
                    rv_cat = self.client.put('/addcategory/'+c, data=post_data, headers=post_headers_user)
        i = 0
        #add games
        r_all_cat = self.client.get('/categories')
        cat = r_all_cat.data.decode('utf8')
        cat = json.loads(cat)
        cat_db = cat['categories']
        age_categories = ['PEGI18','PEGI12','PEGI16','PEGI7']

        with open('store/tests/games.csv', newline='',encoding='utf-8') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',')
            for row in spamreader:
                if i==0:
                    i = i + 1
                    continue
                name = row[0]
                description = row[1]
                description = description[0:89]
                price = int(row[2])                
                categories = row[4]
                is_digital = int(row[5])
                quantity = int(row[6])
                
                cat = categories.split(',')   

                cat_ids = []           
                for c_db in cat_db:
                    for c in cat:
                        if c_db['name'] == c:
                            cat_ids.append(c_db['id'])
                for i in range(0,10):
                    price = random.random() * 250 + 20
                    platform_id = random.randint(1,4)
                    age_category = age_categories[random.randint(1,4) -1]
                    release_date = "2018-12-05"

                    post_data = {'name': name, 'price': price, 'quantity': quantity, 'description': description,
                     'release_date': release_date, 'is_digital': is_digital, 'platform_id': platform_id,
                     'age_category': age_category, 'categories': cat_ids}
                    post_headers_user = {'Authorization': 'Bearer ' +token_admin }

                    rv_cat = self.client.post('/addgame', data=post_data, headers=post_headers_user)

               

                


        

       
        

        

        
       


if __name__ == '__main__':
    unittest.main()