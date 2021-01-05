from contextlib import contextmanager
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
def get_db_read_only():
    mydb = mysql.connector.connect(
    host=db_settings['host'],
    user=db_settings['user'],
    password=db_settings['password'],
    database=db_settings['database']
    )
    return mydb


@contextmanager
def dbTransactionCursor(obj = None):
    db = get_db()
    db.autocommit = False

    cursor = db.cursor()
    try:
        yield cursor
    except Exception:        
        db.rollback()
        raise 
    else:
        db.commit()  
        if obj:
            obj.id = cursor.lastrowid
    finally:        
        if db.is_connected():
            cursor.close()
            db.close()

@contextmanager
def dbCursor():
    db = get_db()
    db.autocommit = False

    cursor = db.cursor()
    try:
        yield cursor
    except Exception:        
        db.rollback()
        raise 
    else:
        db.commit()          
    finally:        
        if db.is_connected():
            cursor.close()
            db.close()

@contextmanager
def dbReadCursor():
    db = get_db_read_only()
    db.autocommit = False

    cursor = db.cursor()
    try:
        yield cursor
    except Exception:        
        db.rollback()
        raise 
    else:
        db.commit()          
    finally:        
        if db.is_connected():
            cursor.close()
            db.close()
