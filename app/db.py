import mysql.connector 

db_settings = {
    'host' : 'localhost',
    'user' : 'root',
    'password' : 'mysqlpass',
    'database' : 'mydb'
}
def get_db():
    mydb = mysql.connector.connect(
    host=db_settings['host'],
    user=db_settings['user'],
    password=db_settings['password'],
    database=db_settings['database']
    )
    return mydb

