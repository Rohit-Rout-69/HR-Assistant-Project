from database.employee_tool import (
    get_employee_details,
    get_leave_balance
)

from actions.leave_request import apply_leave

from actions.hr_ticket import create_ticket

from actions.employee_update import update_email



def employee_details(employee_id: int):

    return get_employee_details(employee_id)



def employee_leave_balance(employee_id: int):

    return get_leave_balance(employee_id)



def submit_leave_request(
    employee_id: int,
    leave_type: str,
    start_date: str,
    end_date: str,
    reason: str
):

    return apply_leave(
        employee_id,
        leave_type,
        start_date,
        end_date,
        reason
    )



def create_hr_ticket(
    employee_id: int,
    subject: str,
    description: str
):

    return create_ticket(
        employee_id,
        subject,
        description
    )



def change_email(
    employee_id: int,
    new_email: str
):

    return update_email(
        employee_id,
        new_email
    )