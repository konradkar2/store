from store.application.utils.db import get_db
from store.application.models.user import UserModel
from store.application.utils.security import encrypt_base64, verifyHash_base64

from store.application.models.category import CategoryModel
from store.application.models.platform import PlatformModel

db = get_db()
cursor = db.cursor()
queries = []
queries.append('delete from users WHERE id > 0')
queries.append('delete from games_categories where id >0')
queries.append('delete from categories where id >0')
queries.append('delete from games where id >0')
queries.append('delete from platforms where id >0')
queries.append('delete from users_transactions where id >0')
queries.append('delete from games_transactions where id >0')
queries.append('delete from games_keys where id >0')


queries.append('ALTER TABLE platforms AUTO_INCREMENT =1;')
queries.append('ALTER TABLE categories AUTO_INCREMENT =1;')

for query in queries:
    cursor.execute(query)
    db.commit()

username = "admin1"
email = "admin1@gmail.com"
password = "admin1"
role = 'admin'

password_hash, salt = encrypt_base64(password)       
user = UserModel(username,email,role,password_hash,salt)
user.save_to_db()

categories = ['action','rpg','rts','sport']

for categoryName in categories:
    category = CategoryModel(categoryName)
    category.save_to_db()

platforms = ['pc','ps4','ps5','xbox-one','xbox-s']
for platformName in platforms:
    platform = PlatformModel(platformName)
    platform.save_to_db()






