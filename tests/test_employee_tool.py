from database.employee_tool import (
    get_employee_details,
    get_leave_balance,
    get_all_employees
)


employee = get_employee_details(101)

print(employee)


leave = get_leave_balance(101)

print(leave)


employees = get_all_employees()

print(employees)