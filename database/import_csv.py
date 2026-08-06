from database.csv_loader import (
    load_employees,
    load_leave_balance
)



def main():


    print(
        "Loading employees..."
    )


    load_employees(
        "data\structured\employees.csv"
    )


    print(
        "Loading leave balance..."
    )


    load_leave_balance(
        "data\structured\leave_balance.csv"
    )


    print(
        "CSV import completed"
    )



if __name__ == "__main__":

    main()