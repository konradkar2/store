import unittest
from store.app.utils.security import encrypt_base64, verifyHash_base64
from store.tests.testingUtils import print_test_time_elapsed, get_random_string

class TestStringHashing(unittest.TestCase):
    def setUp(self):
        # load sample strings
        self.small_str = get_random_string(5)
        self.medium_str = get_random_string(25)
        self.large_str = get_random_string(150)

        self.other_str = get_random_string(25)
        _hash,salt = encrypt_base64(self.other_str)
        self.hash = _hash
        self.salt = salt

    def tearDown(self):
        pass
    
    @print_test_time_elapsed
    def test_verification_time(self):
        str_input = self.other_str
        _hash = self.hash
        salt = self.salt
        result = verifyHash_base64(str_input,_hash,salt)
        assert result == True
    
    @print_test_time_elapsed
    def test_large_str_hash(self):
        str_input = self.large_str
        _hash,salt = encrypt_base64(str_input)
        result = verifyHash_base64(str_input,_hash,salt)
        assert result == True
    
    @print_test_time_elapsed
    def test_medium_str_hash(self):
        str_input = self.medium_str
        _hash,salt = encrypt_base64(str_input)
        result = verifyHash_base64(str_input,_hash,salt)
        assert result == True
    
    @print_test_time_elapsed
    def test_small_str_hash(self):
        str_input = self.small_str
        _hash,salt = encrypt_base64(str_input)
        result = verifyHash_base64(str_input,_hash,salt)
        assert result == True
    @print_test_time_elapsed
    def test_hash_fail(self):
        str_input = self.medium_str
        _hash,salt = encrypt_base64(str_input)
        result = verifyHash_base64(self.other_str,_hash,salt)
        assert result == False


if __name__ == '__main__':
    unittest.main()





print(_hash,salt)





result = verifyHash_base64("żółc",_hash,salt)

assert result == Falsep