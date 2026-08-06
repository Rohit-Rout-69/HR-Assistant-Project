from database.database import get_connection


def create_ticket(

    employee_id: int,

    subject: str,

    description: str

):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(

        """

        INSERT INTO hr_tickets(

            employee_id,

            subject,

            description,

            status

        )

        VALUES(?,?,?,?)

        """,

        (

            employee_id,

            subject,

            description,

            "Open"

        )

    )

    connection.commit()

    ticket_id = cursor.lastrowid

    connection.close()

    return {

        "status":"success",

        "ticket_id":ticket_id,

        "message":"HR ticket created."

    }