import os
import sqlite3
from collections import namedtuple

DBSTRING = os.getenv("DBNAME")


def namedtuple_factory(cursor, row):
    """Returns sqlite rows as named tuples."""
    fields = [col[0] for col in cursor.description]
    Row = namedtuple("Row", fields)
    return Row(*row)


def dict_factory(cursor, row):
    names = [description[0] for description in cursor.description]
    dict_row = {}
    for i, field_name in enumerate(names):
        dict_row[field_name] = row[i]
    return dict_row


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


def get_providers(zipcode, notify):
    sql = "SELECT email, lang, language, category, zipcode FROM providers WHERE zipcode=? AND notify=?"
    sql_args = [zipcode, notify]
    with sqlite3.connect(DBSTRING) as connection:
        connection.row_factory = namedtuple_factory
        cursor = connection.execute(sql, sql_args)
    return cursor.fetchall()


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
        sql = (
            "UPDATE providers SET "
            "zipcode = ?, language = ?, category = ?,"
            "notify = ?"
            " WHERE email = ?"
        )
        sql_args = [zipcode, language, category, notify, email]
        connection.execute(sql, sql_args)
    return "OK"


def insert_seeker_request(
    name, email, phone, language, zipcode, category, additional_info
):

    with sqlite3.connect(DBSTRING) as connection:
        connection.execute(
            "INSERT INTO help_requests"
            "(name, email, phone, language, zipcode, category, additional_info) "
            "VALUES(?, ?, ?, ?, ?, ?, ?)",
            [name, email, phone, language, zipcode, category, additional_info],
        )
    return "OK"


def get_help_requests(email):
    provider = get_provider(email)
    sql = "SELECT hr.*, COALESCE(p.email, '') as assignee FROM help_requests hr " \
          "LEFT JOIN providers p ON p.id = hr.provider_id " \
          "WHERE hr.zipcode=? "
    sql_args = [provider.zipcode]
    with sqlite3.connect(DBSTRING) as connection:
        connection.row_factory = dict_factory
        cursor = connection.execute(sql, sql_args)
        result = cursor.fetchall()
    return result

def get_help_request(id):
    sql = "SELECT hr.*, COALESCE(p.email, '') as assignee FROM help_requests hr " \
          "LEFT JOIN providers p ON p.id = hr.provider_id " \
          "WHERE hr.id=? "
    sql_args = [id]
    with sqlite3.connect(DBSTRING) as connection:
        connection.row_factory = dict_factory
        cursor = connection.execute(sql, sql_args)
        result = cursor.fetchone()
    return result


def check_zip_code(zip_code):
    sql = "SELECT code FROM ZIP_CODES WHERE code=?"
    sql_args = [zip_code]
    with sqlite3.connect("zipcodes.db") as connection:
        cursor = connection.execute(sql, sql_args)
    return cursor.fetchone()


def get_providers_count():
    sql = "SELECT COUNT(*) FROM providers WHERE zipcode > 1"
    with sqlite3.connect(DBSTRING) as connection:
        cursor = connection.execute(sql)
    return cursor.fetchone()


def get_help_requests_count():
    sql = "SELECT COUNT(*) FROM help_requests"
    with sqlite3.connect(DBSTRING) as connection:
        cursor = connection.execute(sql)
    return cursor.fetchone()

def assign_help_request(provider_email, help_request_id):

    with sqlite3.connect(DBSTRING) as connection:
        sql = (
            "UPDATE help_requests SET "
            "provider_id = (SELECT id from providers WHERE email=?) "
            "WHERE id=?"
        )
        sql_args = [provider_email, help_request_id]
        connection.execute(sql, sql_args)
    return get_help_request(help_request_id)

