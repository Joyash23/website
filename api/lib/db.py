import os
import sqlite3
from collections import namedtuple


DBSTRING = os.getenv("DBNAME")


def namedtuple_factory(cursor, row):
    """Returns sqlite rows as named tuples."""
    fields = [col[0] for col in cursor.description]
    Row = namedtuple("Row", fields)
    return Row(*row)


def get_provider(email, token=None):
    sql = "SELECT email, language, category, zipcode FROM providers WHERE email=?"
    sql_args = [email]
    if token:
        sql += " AND token=?"
        sql_args.append(token)
    with sqlite3.connect(DBSTRING) as connection:
        connection.row_factory = namedtuple_factory
        cursor = connection.execute(sql, sql_args)
    return cursor.fetchone()


def insert_or_replace_provider(email, lang, token):

    with sqlite3.connect(DBSTRING) as connection:
        connection.execute(
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
        connection.execute(
            "INSERT INTO seeker_requests"
            "(name, email, phone, language, zipcode, category, additional_info) "
            "VALUES(?, ?, ?, ?, ?, ?, ?)",
            [name, email, phone, language, zipcode, category, additional_info],
        )
    return "OK"


def get_help_requests(email):
    provider = get_provider(email)
    requests_list = []
    sql = "SELECT * FROM seeker_requests WHERE zipcode=?"
    sql_args = [provider.zipcode]
    with sqlite3.connect(DBSTRING) as connection:
        cursor = connection.execute(sql, sql_args)
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