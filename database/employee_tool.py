from database.database import get_connection


def get_employee_details(employee_id: int):
    """
    Get employee information from database.
    """

    connection = get_connection()

    cursor = connection.cursor()


    cursor.execute(
        """
        SELECT
            employee_id,
            name,
            email,
            department,
            designation

        FROM employees

        WHERE employee_id = ?
        """,
        (employee_id,)
    )


    employee = cursor.fetchone()


    connection.close()


    if employee is None:
        return {
            "status": "error",
            "message": "Employee not found"
        }


    return {

        "status": "success",

        "employee_id": employee[0],

        "name": employee[1],

        "email": employee[2],

        "department": employee[3],

        "designation": employee[4]

    }



def get_leave_balance(employee_id: int):
    """
    Get employee leave balance.
    """


    connection = get_connection()

    cursor = connection.cursor()


    cursor.execute(
        """
        SELECT

            sick_leave,
            casual_leave,
            earned_leave

        FROM leave_balance

        WHERE employee_id = ?

        """,
        (employee_id,)
    )


    leave = cursor.fetchone()


    connection.close()


    if leave is None:

        return {

            "status": "error",

            "message": "Leave record not found"

        }



    return {

        "status": "success",

        "employee_id": employee_id,

        "sick_leave": leave[0],

        "casual_leave": leave[1],

        "earned_leave": leave[2]

    }



def get_all_employees():
    """
    Optional:
    Get list of all employees.
    Useful for HR admin queries.
    """


    connection = get_connection()

    cursor = connection.cursor()


    cursor.execute(
        """
        SELECT
            employee_id,
            name,
            department,
            designation

        FROM employees
        """
    )


    employees = cursor.fetchall()


    connection.close()


    return [

        {
            "employee_id": emp[0],
            "name": emp[1],
            "department": emp[2],
            "designation": emp[3]
        }

        for emp in employees

    ]