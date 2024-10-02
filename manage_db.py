import sqlite3

connection = sqlite3.connect('user_data.db')
cursor = connection.cursor()

def init_table():
    init_command = """CREATE TABLE
    users(
        uid TEXT PRIMARY KEY, 
        fname TEXT, 
        lname TEXT, 
        school_uid TEXT, 
        email TEXT
    )
    """
    cursor.execute(init_command)
    connection.commit()

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

def close_connection():
    connection.close()

