from mcp.server.fastmcp import FastMCP

from mcp_server.tools import (
    employee_details,
    employee_leave_balance,
    submit_leave_request,
    create_hr_ticket,
    change_email,
)


mcp = FastMCP(
    "HR Assistant MCP Server"
)


@mcp.tool()
def get_employee_details(employee_id: int):
    """
    Get employee details.
    """

    return employee_details(employee_id)



@mcp.tool()
def get_leave_balance(employee_id: int):
    """
    Get employee leave balance.
    """

    return employee_leave_balance(employee_id)



@mcp.tool()
def apply_leave(
    employee_id: int,
    leave_type: str,
    start_date: str,
    end_date: str,
    reason: str,
):
    """
    Apply leave request.
    """

    return submit_leave_request(
        employee_id,
        leave_type,
        start_date,
        end_date,
        reason,
    )



@mcp.tool()
def raise_hr_ticket(
    employee_id: int,
    subject: str,
    description: str,
):
    """
    Create HR ticket.
    """

    return create_hr_ticket(
        employee_id,
        subject,
        description,
    )



@mcp.tool()
def update_employee_email(
    employee_id: int,
    new_email: str,
):
    """
    Update employee email.
    """

    return change_email(
        employee_id,
        new_email,
    )


if __name__ == "__main__":

    mcp.run(
        transport="stdio"
    )