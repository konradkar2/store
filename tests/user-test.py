from flask import Flask
import unittest
from flask_testing import TestCase


from store.application import app
from store.tests.utils import print_test_time_elapsed, get_random_string



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
    def test_create_user(self):
        user_count = 100
        for i in range(user_count):
            username = 'user-test-' + str(i)
            password = 'user-test-' + str(i)
            email = 'user-test-' + str(i) + '@gmail.com'
            
            post_data = {'username' : username, 'password': password, 'email' : email}
            rv = self.client.post('/register', data=post_data)
            print(rv.data)
            assert rv.status_code == 201
            


if __name__ == '__main__':
    unittest.main()