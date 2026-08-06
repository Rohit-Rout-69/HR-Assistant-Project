from actions.leave_request import apply_leave

from actions.hr_ticket import create_ticket

from actions.employee_update import update_email


print(

    apply_leave(

        101,

        "Sick Leave",

        "2026-08-07",

        "2026-08-08",

        "Fever"

    )

)

print(

    create_ticket(

        101,

        "Laptop Issue",

        "System not booting"

    )

)

print(

    update_email(

        101,

        "rahul.new@company.com"

    )

)