import sqlite3


DATABASE_NAME = "hr_database.db"


def get_connection():

    return sqlite3.connect(
        DATABASE_NAME
    )