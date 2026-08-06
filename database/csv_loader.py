import csv

from database.database import get_connection



def load_employees(csv_file):


    connection = get_connection()

    cursor = connection.cursor()


    with open(
        csv_file,
        "r",
        encoding="utf-8"
    ) as file:


        reader = csv.DictReader(file)


        for row in reader:


            cursor.execute(

            """
            INSERT OR REPLACE INTO employees
            (
                employee_id,
                name,
                email,
                department,
                designation
            )

            VALUES (?,?,?,?,?)

            """,

            (

                row["employee_id"],

                row["name"],

                row["email"],

                row["department"],

                row["designation"]

            )

            )


    connection.commit()

    connection.close()



def load_leave_balance(csv_file):


    connection = get_connection()

    cursor = connection.cursor()



    with open(
        csv_file,
        "r",
        encoding="utf-8"
    ) as file:


        reader = csv.DictReader(file)



        for row in reader:


            cursor.execute(

            """

            INSERT OR REPLACE INTO leave_balance

            (
                employee_id,
                sick_leave,
                casual_leave,
                earned_leave
            )

            VALUES (?,?,?,?)

            """,

            (

                row["employee_id"],

                row["sick_leave"],

                row["casual_leave"],

                row["earned_leave"]

            )

            )


    connection.commit()

    connection.close()