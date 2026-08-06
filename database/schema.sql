CREATE TABLE IF NOT EXISTS employees (

    employee_id INTEGER PRIMARY KEY,

    name TEXT NOT NULL,

    email TEXT UNIQUE,

    department TEXT,

    designation TEXT
);



CREATE TABLE IF NOT EXISTS leave_balance (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    employee_id INTEGER,

    sick_leave INTEGER,

    casual_leave INTEGER,

    earned_leave INTEGER,

    FOREIGN KEY(employee_id)
    REFERENCES employees(employee_id)

);



CREATE TABLE IF NOT EXISTS leave_requests(

    request_id INTEGER PRIMARY KEY AUTOINCREMENT,

    employee_id INTEGER,

    leave_type TEXT,

    start_date TEXT,

    end_date TEXT,

    reason TEXT,

    status TEXT,

    FOREIGN KEY(employee_id)
    REFERENCES employees(employee_id)

);




CREATE TABLE IF NOT EXISTS hr_tickets(

    ticket_id INTEGER PRIMARY KEY AUTOINCREMENT,

    employee_id INTEGER,

    subject TEXT,

    description TEXT,

    status TEXT

);