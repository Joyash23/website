import os
import sqlite3

DBSTRING = os.getenv("DBNAME")


def get_provider(email, token=None):
    sql = "SELECT email FROM providers WHERE email=?"
    sql_args = [email]
    if token:
        sql += " AND token=?"
        sql_args.append(token)
    with sqlite3.connect(DBSTRING) as connection:
        cursor = connection.execute(sql, sql_args)
    return cursor.fetchone()


def insert_or_replace_provider(email, lang, token):

    with sqlite3.connect(DBSTRING) as connection:
        cursor = connection.execute(
            "INSERT OR REPLACE INTO providers(email, lang, token) " "VALUES(?, ?, ?)",
            [email, lang, token],
        )
    return "OK"


def update_provider(email, zipcode, language, category, notify):

    notify = 1 if notify == "on" else 0
    with sqlite3.connect(DBSTRING) as connection:
        sql = "UPDATE providers SET " \
            "zipcode = ?, language = ?, category = ?," \
            "notify = ?" \
            " WHERE email = ?"
        sql_args = [zipcode, language, category, notify, email]
        connection.execute(sql, sql_args)
    return "OK"


def insert_seeker_request(
    name, email, phone, language, zipcode, category, additional_info
):

    with sqlite3.connect(DBSTRING) as connection:
        cursor = connection.execute(
            "INSERT INTO seeker_requests"
            "(name, email, phone, language, zipcode, category, additional_info) "
            "VALUES(?, ?, ?, ?, ?, ?, ?)",
            [name, email, phone, language, zipcode, category, additional_info],
        )
    return "OK"


def get_help_requests():
    requests_list = []
    sql = "SELECT * FROM seeker_requests"
    with sqlite3.connect(DBSTRING) as connection:
        cursor = connection.execute(sql)
        names = [description[0] for description in cursor.description]
    for row in cursor.fetchall():
        dict_row = {}
        for i, field_name in enumerate(names):
            dict_row[field_name] = row[i]
        requests_list.append(dict_row)
    return requests_list


def check_zip_code(zip_code):
    sql = "SELECT code FROM ZIP_CODES WHERE code=?"
    sql_args = [zip_code]
    with sqlite3.connect("zipcodes.db") as connection:
        cursor = connection.execute(sql, sql_args)
    return cursor.fetchone()