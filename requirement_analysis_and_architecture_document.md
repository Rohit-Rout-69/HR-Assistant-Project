# Requirement Analysis and Architecture Document

# HR Assistant AI Agent

Version: 1.1

---

# 1. Introduction

## 1.1 Project Overview

The HR Assistant AI Agent is an AI-powered assistant designed to provide intelligent access to HR information using natural language conversations.

The system combines:

* Large Language Models (LLMs)
* Retrieval-Augmented Generation (RAG)
* Vector databases
* Model Context Protocol (MCP)
* Structured databases
* Role-based access control

The application enables employees to query HR policies while allowing administrators to access both HR documents and employee-specific information, including performing certain HR actions on an employee's behalf.

---

# 2. Problem Statement

Organizations maintain HR information across multiple sources:

* Policy documents
* Employee handbooks
* Leave policies
* Employee databases
* HR management systems

Traditional methods require users to manually search documents or contact HR teams for basic information or routine requests.

The goal of this project is to build an AI assistant that can:

* Understand natural language questions
* Retrieve accurate information from HR documents
* Access structured employee information securely
* Perform basic HR actions on request (leave requests, tickets, contact updates)
* Provide role-based responses
* Reduce manual HR workload

---

# 3. Project Objectives

The main objectives are:

## 3.1 Intelligent HR Querying

Provide conversational access to HR policies and company documents.

Example:

"How many casual leaves are allowed?"

---

## 3.2 Secure Employee Data Access

Allow authorized administrators to retrieve employee information.

Example:

"Show employee details for employee ID 101."

---

## 3.3 HR Action Execution

Allow authorized administrators to perform routine HR actions on an employee's behalf.

Example:

"Apply sick leave for employee 101 from 2026-08-10 to 2026-08-12."

---

## 3.4 Role-Based Access

The system provides different capabilities based on user role.

### User

* Access HR documents only

### Admin

* Access HR documents
* Access structured employee data
* Execute HR actions (leave requests, tickets, email updates)

---

## 3.5 Modular AI Architecture

The system should support future migration from local AI models to cloud-based AI services without changing application logic.

---

# 4. Scope of the Project

## In Scope

The system includes:

* User login interface
* Admin login interface
* HR document processing (ingestion, chunking, embedding)
* Document retrieval (RAG)
* AI-generated responses with cited sources
* Employee database querying (details, leave balance)
* HR action execution (leave request submission, HR ticket creation, email update) — **admin only**
* MCP tool integration
* Streamlit web interface

---

## Out of Scope

The following are not implemented currently:

* Payroll processing
* Attendance tracking
* Leave approval / rejection workflow (leave requests are recorded as "Pending" only — no approval logic exists)
* Real HR management system integration
* Enterprise identity providers (LDAP/SSO)
* Self-service HR actions for regular users (currently admin-only)
* Real authentication (current login is a placeholder — see Section 14)

---

# 5. User Roles

# 5.1 Normal User

A normal user represents an employee.

Permissions:

| Feature                  | Access |
| ------------------------ | ------ |
| Login                    | Yes    |
| HR Policy Search         | Yes    |
| Document-based Questions | Yes    |
| Employee Database        | No     |
| Apply Leave / Raise Ticket / Update Email | No |
| MCP Tools                | No     |

---

# 5.2 Administrator

An administrator manages HR information.

Permissions:

| Feature                                   | Access |
| ------------------------------------------ | ------ |
| Login                                      | Yes    |
| HR Policy Search                           | Yes    |
| Employee Details Lookup                    | Yes    |
| Leave Balance Lookup                       | Yes    |
| Apply Leave (on behalf of employee)        | Yes    |
| Raise HR Ticket (on behalf of employee)    | Yes    |
| Update Employee Email                      | Yes    |
| MCP Tools                                  | Yes    |

> Note: Admin actions currently apply to any `employee_id` supplied — there is
> no check restricting an admin to a specific department or employee scope
> (see Section 14).

---

# 6. Functional Requirements

# FR-01: User Authentication

The system shall provide login functionality.

Users must provide:

* Username
* Password
* Role selection

The system shall identify whether the user is:

* User
* Administrator

---

# FR-02: HR Document Question Answering

The system shall allow users to ask questions about HR policies.

Example:

Input:

```
What is the sick leave policy?
```

Output:

```
Employees are allowed 7 sick leaves per year.
```

---

# FR-03: Document Retrieval

The system shall retrieve relevant information from HR documents.

The retrieval process shall:

1. Convert documents into chunks
2. Generate embeddings
3. Store embeddings
4. Retrieve relevant chunks
5. Generate answers grounded in the retrieved context

---

# FR-04: Employee Data Access

Administrators shall be able to query employee information.

Examples:

```
Show employee details.
```

```
What is employee 101's leave balance?
```

---

# FR-05: MCP Tool Execution

The system shall use MCP tools to access and modify structured information.

MCP provides a controlled interface between:

* AI agent
* Business logic (database reads and writes)
* Database

---

# FR-06: Source Information

For document-based answers, the system shall provide:

* Document name
* Page number

---

# FR-07: HR Action Execution

Administrators shall be able to perform the following actions through the assistant:

* Submit a leave request on behalf of an employee (recorded with status "Pending")
* Raise an HR ticket on behalf of an employee (recorded with status "Open")
* Update an employee's email address

These actions shall be executed only through MCP tools, not by direct database access from the agent.

---

# 7. Non-Functional Requirements

# Performance

The system should:

* Provide responses within acceptable time
* Efficiently retrieve relevant documents
* Handle multiple user queries

---

# Security

The system should:

* Restrict employee data access to administrators
* Separate user and admin permissions
* Prevent unauthorized database access

> Current status: role separation is enforced at the application/agent level,
> but login itself does not verify credentials. See Section 14.

---

# Scalability

The architecture should support:

* Additional MCP tools
* More documents
* Cloud LLM migration

---

# Maintainability

The system should have:

* Modular components
* Separate providers
* Independent services

---

# Reliability

The system should:

* Handle failures gracefully
* Maintain consistent responses

---

# 8. System Architecture

## High-Level Architecture

```
                              User
                               |
                        Streamlit UI
                               |
                +--------------+--------------+
                |                             |
           role = user                   role = admin
                |                             |
           User Agent                   Admin Agent
                |                             |
                |                     LangChain Agent
                |                             |
                |              +--------------+--------------+
                |              |                             |
            RAG Tool       RAG Tool                     MCP Tools
                |              |                             |
                |              |                        MCP Client
                |              |                             |
                +------> ChromaDB <-----------------+   (spawns subprocess)
                               |                          |
                          HR Documents                MCP Server
                                                            |
                                                  Database & Action Layer
                                                            |
                                                    SQLite Database

           Both agent paths call the LLM through
                    providers/llm_provider.py
                         (Ollama, local)
```

---

# 9. Architecture Components

# 9.1 User Interface Layer

Technology:

```
Streamlit
```

Responsibilities:

* User login
* Admin login
* Chat interface
* Display responses
* Display sources

---

# 9.2 Agent Layer

Technology:

```
LangChain Agents
```

Responsibilities:

* Understand user intent
* Select appropriate tools
* Generate responses

---

## User Agent

Purpose:

Handles employee queries.

Available capability:

```
RAG Search only
```

---

## Admin Agent

Purpose:

Handles administrator queries.

Available capabilities:

```
RAG Search (native tool)
MCP Tools (employee data read + HR action write, 5 tools)
```

Total tools available to the admin agent: **6** (5 MCP tools + 1 RAG tool).

---

# 9.3 RAG Layer

The RAG pipeline handles document-based knowledge retrieval.

Components:

```
HR Documents
      |
Document Loader
      |
Text Splitter
      |
Embedding Model
      |
ChromaDB
      |
Retriever
      |
LLM Response
```

---

# 9.4 Embedding Layer

Technology:

```
Ollama Embeddings (default)
```

Purpose:

Convert text into numerical vectors.

Used for:

* Similarity search
* Document retrieval

The embedding provider is abstracted so it can be swapped for a cloud provider (e.g. Azure) via configuration only.

---

# 9.5 Vector Database

Technology:

```
ChromaDB
```

Responsibilities:

* Store document embeddings
* Perform similarity search
* Return relevant context

---

# 9.6 MCP Layer

Model Context Protocol provides structured tool access between the admin agent and the database.

Architecture:

```
LangChain Admin Agent
        |
MCP Client (spawns MCP Server as a subprocess over stdio)
        |
MCP Server (registers 5 tools)
        |
Database & Action Layer
 (reads: employee_tool.py | writes: actions/*.py)
        |
SQLite
```

The agent never accesses SQLite directly — every structured-data operation goes through an MCP tool call.

---

# 10. MCP Tools

The MCP server exposes **5 tools**, available only to the admin agent.

## Tool 1: Employee Details Tool

Purpose:

Retrieve employee information.

```
get_employee_details(employee_id)
```

Returns:

* Employee ID
* Name
* Email
* Department
* Designation

---

## Tool 2: Leave Balance Tool

Purpose:

Retrieve employee leave data.

```
get_leave_balance(employee_id)
```

Returns:

* Sick leave
* Casual leave
* Earned leave

---

## Tool 3: Apply Leave Tool

Purpose:

Submit a leave request on behalf of an employee.

```
apply_leave(employee_id, leave_type, start_date, end_date, reason)
```

Returns:

* Request ID
* Status ("Pending")

Note: this only records the request — there is currently no approval workflow.

---

## Tool 4: HR Ticket Tool

Purpose:

Raise an HR support ticket on behalf of an employee.

```
raise_hr_ticket(employee_id, subject, description)
```

Returns:

* Ticket ID
* Status ("Open")

---

## Tool 5: Employee Email Update Tool

Purpose:

Update an employee's email address.

```
update_employee_email(employee_id, new_email)
```

Returns:

* Confirmation status

---

# 11. Data Architecture

## Document Data Flow

```
HR Documents (PDFs)
      |
Ingestion
      |
Chunking
      |
Embedding
      |
ChromaDB
```

---

## Structured Data Flow (initial seed)

```
Employee CSV + Leave Balance CSV
      |
Database Schema Init
      |
CSV Import
      |
SQLite Database
      |
MCP Tools (read/write)
      |
Admin Agent
```

---

# 12. Technology Stack

| Layer            | Technology                         |
| ----------------- | ----------------------------------- |
| Frontend          | Streamlit                          |
| Backend Language  | Python                             |
| AI Framework      | LangChain                          |
| LLM               | Ollama (local); Azure-ready         |
| Embeddings        | Ollama Embeddings (local); Azure-ready |
| Vector Database   | ChromaDB                           |
| Database          | SQLite                             |
| Tool Protocol     | MCP (stdio transport)              |
| Package Manager   | uv                                  |

---

# 13. Security Architecture

Security controls:

## Role Separation

Users cannot access:

* Employee database
* MCP tools

Admins can access:

* Documents
* Employee information
* HR action tools

---

## Data Isolation

The system separates:

* Public HR knowledge (documents, via RAG)
* Private employee data (database, via MCP tools)

---

# 14. Current Implementation Notes

This section documents known gaps between the design above and the current build, so the architecture document doesn't overstate what's implemented.

* **Login is a placeholder.** Any non-empty username/password combination is
  accepted; there is no credential verification. Role separation (user vs.
  admin) is enforced after login, but authentication itself is not real.
* **No per-employee access scoping.** An admin can query or modify data for
  any `employee_id`, with no binding to the admin's own identity or
  department.
* **No leave approval workflow.** `apply_leave` only inserts a record with
  status "Pending" — nothing in the system currently transitions it to
  "Approved" or "Rejected".
* **HR actions are admin-only.** Regular users cannot submit their own leave
  requests or tickets through the assistant in the current build.

These are intentional simplifications for the current version and are
tracked under Future Enhancements (Section 16).

---

# 15. Deployment Architecture

Current deployment:

```
Local Machine
      |
Streamlit Application
      |
Python Backend
      |
Ollama Server
      |
SQLite Database
```

---

Future deployment:

```
Cloud Environment
      |
Web Application
      |
API Backend
      |
Cloud LLM
      |
Cloud Database
```

---

# 16. Future Enhancements

Possible improvements:

## Authentication

* Real credential verification
* JWT authentication
* LDAP / SSO integration
* Per-employee access scoping for admins

---

## Database

Replace SQLite with:

* PostgreSQL
* MySQL

---

## AI Improvements

Add:

* Conversation memory
* Feedback system
* Response evaluation

---

## MCP Expansion

Additional tools:

* Leave approval / rejection workflow
* Employee onboarding
* Attendance reports
* Payroll information
* Self-service leave/ticket actions for regular users

---

# 17. Conclusion

The HR Assistant AI Agent provides a scalable AI architecture for enterprise HR automation.

The combination of:

* LangChain agents
* RAG
* Vector search
* MCP tools (read and write)
* Structured databases

creates a flexible system capable of handling both document-based knowledge retrieval and real-time business data access and updates.

The modular architecture allows future migration from local AI models to cloud-based enterprise AI solutions, and the current implementation notes (Section 14) provide a clear list of gaps to close before production use.
