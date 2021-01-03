from flask import Flask
import unittest
from flask_testing import TestCase
import json

from store.application import app
from store.tests.utils import print_test_time_elapsed, get_random_string
from store.application.utils.db import dbTransactionCursor
from store.application.models.user import UserModel
from store.application.models.category import CategoryModel
from store.application.models.platform import PlatformModel
from store.application.resources.user import UserLogin
from store.application.resources.game_admin import AddGame
from store.application.utils.security import encrypt_base64, verifyHash_base64


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
  
    # @print_test_time_elapsed
    # def test_create_user(self):
    #     username = 'user-test'
    #     password = 'user-test'
    #     email = 'user-test@gmail.com'
    #
    #     with dbTransactionCursor(self) as cursor:
    #         print("Czyszczenie bazy po testach")
    #         query = "delete from users where name like 'user-test%'"
    #         cursor.execute(query)
    #
    #     try:
    #         print("Poprawne tworzenie usera")
    #         post_data = {'username' : username, 'password': password, 'email' : email}
    #         rv = self.client.post('/register', data=post_data)
    #         print(rv.data)
    #         assert rv.status_code == 201
    #     except:
    #         pass
    #
    #     try:
    #         print("Tworzenie usera bez hasła")
    #         post_data = {'username': username, 'password': '', 'email': email}
    #         rv = self.client.post('/register', data=post_data)
    #         print(rv.data)
    #         assert rv.status_code == 201
    #     except:
    #         pass
    #
    #     try:
    #         print("Tworzenie usera bez nazwy")
    #         post_data = {'username': '', 'password': password, 'email': email}
    #         rv = self.client.post('/register', data=post_data)
    #         print(rv.data)
    #         assert rv.status_code == 201
    #     except:
    #         pass
    #
    #     try:
    #         print("Tworzenie usera z istniejącym mailem")
    #         post_data = {'username': username + 'abc', 'password': password, 'email': email}
    #         rv = self.client.post('/register', data=post_data)
    #         print(rv.data)
    #         assert rv.status_code == 201
    #     except:
    #         pass
    #
    #     try:
    #         print("Tworzenie usera z istniejącym usernamem")
    #         post_data = {'username': username, 'password': password, 'email': email + 'abc'}
    #         rv = self.client.post('/register', data=post_data)
    #         print(rv.data)
    #         assert rv.status_code == 201
    #     except:
    #         pass
    #
    #     print("Stworzenie 5 userów")
    #     user_count = 5
    #     for i in range(user_count):
    #         username = 'user-test-' + str(i)
    #         password = 'user-test-' + str(i)
    #         email = 'user-test-' + str(i) + '@gmail.com'
    #
    #         post_data = {'username' : username, 'password': password, 'email' : email}
    #         rv = self.client.post('/register', data=post_data)
    #         print(rv.data)
    #         assert rv.status_code == 201
    #         print(UserModel.find_by_username(username).username)
    #
    #         post_data = {'username': username, 'password': password}
    #         login = self.client.post('/auth', data=post_data)
    #         print(login.data)

    @print_test_time_elapsed
    def test_gamemodel(self):
        test_cat = CategoryModel("Kategoria testowa")
        # test_cat.save_to_db()

        test_platform = PlatformModel("PC")
        # test_platform.save_to_db()

        username = "test-admin"
        email = "testadmin@gmail.com"
        password = "admin"
        role = 'admin'

        password_hash, salt = encrypt_base64(password)
        admin = UserModel(username, email, role, password_hash, salt)
        # admin.save_to_db()

        post_data = {'username' : username, 'password' : password}
        login = self.client.post('/auth', data=post_data)
        print(login.data)
        my_json = login.data.decode('utf8').replace("'", '"')
        print(my_json[18:329])
        #
        # name = "Tomb Raider"
        # price = 200.0
        # quantity = "10"
        # description = "Good game"
        # release_date = "Jutro"
        # is_digital = False
        # platform_id = 1
        # age_category = "PEGI 3"
        # categories = "Kategoria testowa"
        #
        # post_data = {'name' : name, 'price' : price, 'quantity' : quantity, 'description' : description,
        #              'release_date' : release_date, 'is_digital' : is_digital, 'platform_id' : platform_id,
        #              'age_category' : age_category, 'categories' : categories}
        #
        # rv = self.client.post('/addgame', data=post_data)
        # assert rv.status_code == 201



if __name__ == '__main__':
    unittest.main()