import sqlite3
import os

dbpath = r'db' 
if not os.path.exists(dbpath):
    os.makedirs(dbpath)
connection = sqlite3.connect(f'{dbpath}/user_data.sqlite')
cursor = connection.cursor()

def init_table():
    init_users_command = """CREATE TABLE IF NOT EXISTS
    users(
        uid TEXT PRIMARY KEY, 
        fname TEXT, 
        lname TEXT, 
        school_uid TEXT, 
        email TEXT
    )
    """
    init_bookings_command = """CREATE TABLE IF NOT EXISTS
    bookings(
        bookId TEXT PRIMARY KEY,
        day TEXT,
        start_time TEXT,
        end_time TEXT,
        discord_uid TEXT,
        FOREIGN KEY("discord_uid") REFERENCES "users"("uid")
    )
    """
    cursor.execute(init_users_command)
    cursor.execute(init_bookings_command)
    connection.commit()
init_table()

def delete_table():
    drop_command = """DROP TABLE users
    """
    cursor.execute(drop_command)
    connection.commit()

def create_profile(uid, fname, lname, school_uid, email):
    create_command = f"""INSERT INTO users
        VALUES(
            '{uid}', 
            '{fname}', 
            '{lname}', 
            '{school_uid}', 
            '{email}'
        )
    """
    cursor.execute(create_command)
    connection.commit()

def delete_profile(uid):
    if user_exist(uid):
        delete_command = f"DELETE FROM users WHERE uid = {uid}"
        cursor.execute(delete_command)
        connection.commit()
        return True
    else:
        return False

def update_profile(uid, attribute, new_value):
    update_command = f"""UPDATE users
        SET {attribute} = '{new_value}'
        WHERE uid = '{uid}'
    """
    cursor.execute(update_command)
    connection.commit()

def user_exist(uid):
    find_user_command = f"SELECT EXISTS(SELECT 1 FROM users WHERE uid = '{uid}')"
    cursor.execute(find_user_command)
    return cursor.fetchmany()[0][0] == 1

def get_all_data():
    view_command = """SELECT * FROM users
    """
    cursor.execute(view_command)
    return cursor.fetchmany()

def get_user(uid):
    get_command = f"SELECT * FROM users WHERE uid = '{uid}'"
    cursor.execute(get_command)
    return convert_tuple_to_dict(cursor.fetchmany()[0])

def convert_tuple_to_dict(tuple):
    output = {
        'uid': tuple[0],
        'fname': tuple[1],
        'lname': tuple[2],
        'school_uid': tuple[3],
        'email': tuple[4]
    }
    return output

def add_booking(bookId, day, start_time, end_time, uid):
    add_command = f"""INSERT INTO bookings
        VALUES(
            '{bookId}',
            '{day}',
            '{start_time}',
            '{end_time}',
            '{uid}'
        )
    """
    cursor.execute(add_command)
    connection.commit()

def get_all_bookings(uid):
    get_command = f"SELECT * FROM bookings WHERE discord_uid='{uid}' AND day >= date('now','localtime')" 
    cursor.execute(get_command)
    return cursor.fetchall()

def delete_booking(bookId):
    delete_command = f"DELETE FROM bookings WHERE bookId='{bookId}'"
    cursor.execute(delete_booking)
    connection.commit()

def close_connection():
    connection.close()

if __name__ == '__main__':
    init_table()
    close_connection()
