from langchain.tools import tool

from rag.rag_tool import search_hr_policy

from database.employee_tool import (
    get_employee_details,
    get_leave_balance
)

from actions.leave_request import apply_leave
from actions.hr_ticket import create_ticket
from actions.employee_update import update_email


#hr policy tool
@tool
def hr_policy_tool(question: str) -> str:
    """
    Search HR policy documents.
    """

    return search_hr_policy(question)



#employee tool
@tool
def employee_tool(
    employee_id: int,
    query_type: str
):
    """
    Query employee information.

    query_type:

    details

    leave_balance
    """

    if query_type == "details":

        return get_employee_details(
            employee_id
        )

    if query_type == "leave_balance":

        return get_leave_balance(
            employee_id
        )

    return "Invalid query type."



#hr actions tool
@tool
def hr_action_tool(
    action: str,
    employee_id: int,
    **kwargs
):
    """
    Perform HR actions.
    """

    if action == "apply_leave":

        return apply_leave(

            employee_id,

            kwargs["leave_type"],

            kwargs["start_date"],

            kwargs["end_date"],

            kwargs["reason"]

        )

    if action == "create_ticket":

        return create_ticket(

            employee_id,

            kwargs["subject"],

            kwargs["description"]

        )

    if action == "update_email":

        return update_email(

            employee_id,

            kwargs["new_email"]

        )

    return "Unknown action."





TOOLS = [

    hr_policy_tool,

    employee_tool,

    hr_action_tool

]