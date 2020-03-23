import sqlite3
import os


CREATE_SQL = [
    """
CREATE TABLE IF NOT EXISTS providers
    (email TEXT, lang TEXT , token TEXT,
    verified INTEGER DEFAULT 0, zipcode INTEGER,
    language TEXT, category TEXT, notify INTEGER
    );
""",
    """
CREATE UNIQUE INDEX IF NOT EXISTS idx_contacts_email
    ON providers (email);
""",
    """
CREATE TABLE IF NOT EXISTS seeker_requests
    (name TEXT, email TEXT, phone TEXT, language TEXT, zipcode INTEGER,
    category TEXT, additional_info TEXT);
""",
]


def start():
    setup_database()


def setup_database():
    """
    Create the `user_string` table in the database
    on server startup
    """
    DB_STRING = os.getenv("DBNAME", "test.db")
    with sqlite3.connect(DB_STRING) as con:
        for sql in CREATE_SQL:
            con.execute(sql)
