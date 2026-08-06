from database.database import get_connection


def update_email(

    employee_id: int,

    new_email: str

):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(

        """

        UPDATE employees

        SET email=?

        WHERE employee_id=?

        """,

        (

            new_email,

            employee_id

        )

    )

    connection.commit()

    connection.close()

    return {

        "status":"success",

        "message":"Email updated."

    }