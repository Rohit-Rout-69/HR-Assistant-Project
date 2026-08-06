from database.database import get_connection


def apply_leave(
    employee_id: int,
    leave_type: str,
    start_date: str,
    end_date: str,
    reason: str
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO leave_requests(

            employee_id,

            leave_type,

            start_date,

            end_date,

            reason,

            status

        )

        VALUES(?,?,?,?,?,?)
        """,

        (

            employee_id,

            leave_type,

            start_date,

            end_date,

            reason,

            "Pending"

        )

    )

    connection.commit()

    request_id = cursor.lastrowid

    connection.close()

    return {

        "status":"success",

        "request_id":request_id,

        "message":"Leave request submitted successfully."

    }