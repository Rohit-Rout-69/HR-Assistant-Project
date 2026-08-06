import sqlite3

from database.database import DATABASE_NAME



def initialize_database():

    connection = sqlite3.connect(
        DATABASE_NAME
    )

    cursor = connection.cursor()


    with open(
        "database/schema.sql",
        "r"
    ) as file:

        schema = file.read()


    cursor.executescript(
        schema
    )


    connection.commit()

    connection.close()


    print(
        "Database initialized"
    )



if __name__ == "__main__":

    initialize_database()