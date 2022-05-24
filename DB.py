import sqlite3


def update_table(id, selection, value):
    try:
        sqlite_connection = sqlite3.connect('database.db')
        cursor = sqlite_connection.cursor()

        sql_update_query = f"""Update USER set {selection} = '{value}' where id = {id}"""
        cursor.execute(sql_update_query)
        sqlite_connection.commit()
        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()

def get_value(selection, value):
    try:
        sqlite_connection = sqlite3.connect('database.db')
        with sqlite_connection:
            data = sqlite_connection.execute(f"SELECT * FROM USER WHERE {selection} = {value}")
            for row in data:
                i = row
        try:
            return i
        except:
            return 0
    except sqlite3.Error as error:
        print(error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()

def get_is(selection, value):
    try:
        sqlite_connection = sqlite3.connect('database.db')
        with sqlite_connection:
            data = sqlite_connection.execute(f"SELECT * FROM USER WHERE {selection} = {value}")
            for row in data:
                i = row
        try:
            i + i
            return 1
        except:
            return 0
    except sqlite3.Error as error:
        print(error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()


def add(id, name='', requests='', last_request='', last_active='', root=0):
    sqlite_connection = sqlite3.connect('database.db')
    _ = 'INSERT INTO USER (id, name, requests, last_request, last_active, root) values(?, ?, ?, ?, ?, ?)'
    data = [(id, name, requests, last_request, last_active, root)]
    try:
        with sqlite_connection:
            sqlite_connection.executemany(_, data)
        return 1
    except:
        return 0


def delete(selection, value):
    try:
        sqlite_connection = sqlite3.connect('database.db')
        cursor = sqlite_connection.cursor()

        sql_delete_query = f"""DELETE from USER where {selection} = {value}"""
        cursor.execute(sql_delete_query)
        sqlite_connection.commit()
        cursor.close()
        return 1

    except:
        return 0
    finally:
        if sqlite_connection:
            sqlite_connection.close()
