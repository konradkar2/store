import mysql.connector 

db_settings = {
    'host' : 'localhost',
    'user' : 'root',
    'password' : 'mysqlpass',
}
def get_db():
    mydb = mysql.connector.connect(
    host=db_settings['host'],
    user=db_settings['user'],
    password=db_settings['password']
    )
    return mydb

