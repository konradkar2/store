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
class UserTest(TestCase):
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
        
        
        name = "Tomb Raider"
        price = 200.0
        quantity = "10"
        description = "Good game"
        release_date = "Jutro"
        is_digital = 1
        platform_id = 1
        age_category = "PEGI 3"
        categories = 1

        post_data = {'name': name, 'price': price, 'quantity': quantity, 'description': description,
                     'release_date': release_date, 'is_digital': is_digital, 'platform_id': platform_id,
                     'age_category': age_category, 'categories': categories}

        post_headers_user = {'Authorization': 'Bearer ' +token_admin }
        try:
            rv_user = self.client.post('/addgame', data=post_data, headers=post_headers_user)
        except:
            pass

        print("Tworzenie 2 cyfrowych gier")
        post_headers = {'Authorization': 'Bearer ' + token_admin}
        rv = self.client.post('/addgame', data=post_data, headers=post_headers)
        rv = self.client.post('/addgame', data=post_data, headers=post_headers)

        print("Tworzenie 1 wersji pudełkowej")
        post_data['is_digital'] = 0
        rv = self.client.post('/addgame', data=post_data, headers=post_headers)

        id1 = 81  # Cyfrowa
        id2 = 82  # Cyfroowa
        id3 = 83  # Pudełko
        fake_id = 999

        

        print("Poprawne dodanie klucza")
        klucz = "losowy klucz"
        post_data = {'game_id': id1, 'key': klucz}
        rv = self.client.post('/addkey', data=post_data, headers=post_headers)

        print("Dodanie klucza do wersji pudełkowej")
        try:
            klucz2 = "losowy klucz 2"
            post_data = {'game_id': id3, 'key': klucz2}
            rv = self.client.post('/addkey', data=post_data, headers=post_headers)
        except:
            pass

        print("Powtórne użycie tego samego klucza")
        post_data = {'game_id': id2, 'key': klucz}
        rv = self.client.post('/addkey', data=post_data, headers=post_headers)

        print("Dodanie klucza do nieistniejącej gry")
        post_data = {'game_id': fake_id, 'key': klucz2}
        rv = self.client.post('/addkey', data=post_data, headers=post_headers)

        resetDb()
       


if __name__ == '__main__':
    unittest.main()