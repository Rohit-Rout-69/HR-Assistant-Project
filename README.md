# HR Assistant AI Agent

An AI-powered HR Assistant built using **LangChain, Ollama, Retrieval-Augmented Generation (RAG), and the Model Context Protocol (MCP)**.

The system allows users and administrators to interact with HR information using natural language.

The application supports:

* HR policy question answering using RAG
* Employee information retrieval and HR actions using MCP tools
* Role-based access control (user vs. admin)
* Local LLM and embedding models through Ollama
* A provider layer ready for future migration to cloud AI (Azure)

---

# 1. Project Overview

The HR Assistant AI Agent provides HR support by combining two different information sources:

## Unstructured Data

HR documents such as:

* Employee handbook
* Leave policy
* Compliance documents
* Exit procedure

These are processed through a RAG pipeline (chunked, embedded, and stored in a vector database).

---

## Structured Data

Employee records stored in SQLite:

* Employee details (name, email, department, designation)
* Leave balances (sick / casual / earned leave)
* Leave requests
* HR tickets

This data is accessed through MCP tools on the admin path.

---

# 2. System Architecture

```
                         User
                          |
                    Streamlit UI (ui/app.py)
                          |
              +-----------+-----------+
              |                       |
         role = user             role = admin
              |                       |
        User Agent              Admin Agent
     (agent/user_agent.py)   (agent/admin_agent.py)
              |                       |
              |                 LangChain Agent (agent/agent.py)
              |                       |
              |              +--------+--------+
              |              |                 |
          RAG Tool       RAG Tool          MCP Client
    (rag/rag_tool.py) (agent/tools.py)  (mcp_client/client.py)
              |              |                 |
          ChromaDB       ChromaDB      spawns subprocess (stdio)
              |              |                 |
       HR Documents   HR Documents        MCP Server
                                      (mcp_server/server.py)
                                             |
                                    database/employee_tool.py
                                          actions/*.py
                                             |
                                      SQLite Database
                                     (hr_database.db)

                    Both paths call the LLM through
                       providers/llm_provider.py
                              (Ollama)
```

---

# 3. Features

## User Features

Users who log in with role `user` can:

1. Ask questions about HR policies
2. Search HR documents
3. Receive answers with document sources (file + page number)

Examples:

```
What is the sick leave policy?
How many casual leaves are allowed?
What is the notice period?
```

Users cannot access the employee database or perform HR actions.

---

## Admin Features

Administrators (role `admin`) can:

1. Search HR documents (same RAG tool as users)
2. Look up employee details and leave balances
3. Submit a leave request on an employee's behalf
4. Raise an HR ticket
5. Update an employee's email address

All of this is exposed to the agent as MCP tools, plus one native RAG tool.

Examples:

```
What is the maternity leave policy?
Show employee 101 details.
How many leaves does employee 101 have?
Apply sick leave for employee 101 from 2026-08-10 to 2026-08-12, reason: fever.
Raise a ticket for employee 101 about a payroll issue.
Update employee 101's email to new.email@company.com
```

> **Note:** In the current implementation, leave requests, ticket creation, and
> email updates are only exposed through the **admin** agent (via MCP). Regular
> users cannot submit these themselves — this is worth revisiting if employees
> should be able to self-serve these actions.

---

# 4. Technology Stack

| Component              | Technology                       |
| ----------------------- | --------------------------------- |
| Programming Language    | Python 3.11+                      |
| UI Framework            | Streamlit                         |
| Agent Framework         | LangChain (`create_agent`)        |
| LLM Provider            | Ollama (local), Azure OpenAI-ready |
| Embedding Provider      | Ollama (local), Azure OpenAI-ready |
| Vector Database         | ChromaDB                          |
| Structured Database     | SQLite                            |
| Document Loading/Splitting | LangChain + `pypdf`             |
| Tool Protocol            | Model Context Protocol (MCP), stdio transport |
| Dependency Management    | uv                               |

---

# 5. Project Structure

```
HR Assistant Project/
│
├── agent/
│   ├── agent.py            # builds the admin LangChain agent (MCP + RAG tools)
│   ├── admin_agent.py      # ask_admin() entry point used by the UI
│   ├── user_agent.py       # returns the RAG-only function for user role
│   ├── tools.py            # native LangChain tools (hr_policy_tool is the one actually used)
│   └── prompt.py           # SYSTEM_PROMPT for the admin agent
│
├── rag/
│   ├── ingestion.py        # loads PDFs from data/documents
│   ├── splitter.py         # chunks documents
│   ├── build_index.py      # runs ingestion + splitting + embedding (main entry point)
│   ├── vectorstore.py      # creates the Chroma vector store
│   ├── retriever.py        # loads the Chroma store for querying
│   ├── prompts.py          # RAG_PROMPT template
│   └── rag_tool.py         # search_hr_policy() — the actual RAG chain
│
├── mcp_server/
│   ├── server.py           # FastMCP server, 5 registered tools, stdio transport
│   └── tools.py            # wrapper functions calling database/ and actions/
│
├── mcp_client/
│   └── client.py           # MultiServerMCPClient — spawns mcp_server as a subprocess
│
├── providers/
│   ├── llm_provider.py       # get_llm() — Ollama or Azure, based on .env
│   └── embedding_provider.py # get_embeddings() — Ollama or Azure, based on .env
│
├── database/
│   ├── schema.sql           # employees, leave_balance, leave_requests, hr_tickets
│   ├── database.py          # get_connection()
│   ├── init_db.py           # creates tables from schema.sql
│   ├── csv_loader.py        # load_employees(), load_leave_balance()
│   ├── import_csv.py        # runs both CSV loaders
│   └── employee_tool.py     # get_employee_details(), get_leave_balance(), get_all_employees()
│
├── actions/
│   ├── leave_request.py     # apply_leave()
│   ├── hr_ticket.py         # create_ticket()
│   └── employee_update.py   # update_email()
│
├── security/
│   └── roles.py             # UserRole enum (user / admin)
│
├── data/
│   ├── documents/           # HR policy PDFs
│   └── structured/          # employees.csv, leave_balance.csv
│
├── ui/
│   ├── app.py               # Streamlit app: login + chat, routes by role
│   └── auth.py              # standalone login helper
│
├── tests/                   # manual smoke-test scripts (not automated pytest suites)
│
├── config.py                 # reads .env, exposes provider settings
├── hr_database.db            # SQLite database file (generated)
├── chroma_db/                # Chroma vector store (generated)
├── .env                       # environment configuration (not committed)
├── pyproject.toml
└── README.md
```

---

# 6. Requirements

## Software Requirements

Install:

1. Python 3.11+
2. Ollama
3. uv

---

# 7. Install Ollama

Download and install Ollama:

https://ollama.com

Verify installation:

```bash
ollama --version
```

---

# 8. Download Required Models

This project uses Ollama for both the language model and the embedding model.

Pull the LLM:

```bash
ollama pull llama3.2
```

Pull the embedding model:

```bash
ollama pull nomic-embed-text
```

Verify models:

```bash
ollama list
```

---

# 9. Setup Project Environment

Navigate to the project directory:

```bash
cd "HR Assistant Project"
```

Create a virtual environment:

```bash
uv venv
```

Activate it.

Windows:

```powershell
.venv\Scripts\activate
```

Linux/Mac:

```bash
source .venv/bin/activate
```

---

# 10. Install Dependencies

```bash
uv sync
```

---

# 11. Configure Environment

Configuration is read from a **`.env`** file at the project root (via `python-dotenv`) —
you do not edit `config.py` directly. Create `.env` with:

```env
# Provider selection
LLM_PROVIDER=ollama
EMBEDDING_PROVIDER=ollama

# Ollama configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_LLM_MODEL=llama3.2
OLLAMA_EMBEDDING_MODEL=nomic-embed-text

# Azure configuration (optional, only needed if LLM_PROVIDER/EMBEDDING_PROVIDER = azure)
AZURE_ENDPOINT=
AZURE_API_KEY=
AZURE_API_VERSION=
AZURE_CHAT_DEPLOYMENT=
AZURE_EMBEDDING_DEPLOYMENT=
```

---

# 12. Prepare HR Documents

Place HR policy PDFs inside:

```
data/documents/
```

Example:

```
data/
└── documents/
     ├── Holiday and Leave Policy 2026.pdf
     ├── HR Induction Handbook.pdf
     ├── Mandatory Compliance.pdf
     └── Employee Exit Procedure.pdf
```

Any `.pdf` file placed in this folder is picked up automatically — file names don't need to match a specific format.

---

# 13. Build the RAG Index

`rag/build_index.py` handles the full pipeline (loading, splitting, embedding, storing) in one command:

```bash
uv run python -m rag.build_index
```

This will:

1. Load HR documents from `data/documents/`
2. Split documents into chunks
3. Generate embeddings using Ollama
4. Store embeddings in ChromaDB (`chroma_db/`)

> You do **not** need to run `rag.ingestion` separately — it's called internally by `build_index.py`.

---

# 14. Initialize the Database and Import Employee Data

First, create the database tables:

```bash
uv run python -m database.init_db
```

Then place your CSV files inside:

```
data/structured/
```

`employees.csv` needs these columns:

```
employee_id,name,email,department,designation
101,John,john@company.com,IT,Developer
```

`leave_balance.csv` needs these columns:

```
employee_id,sick_leave,casual_leave,earned_leave
101,7,8,5
```

Run the import script:

```bash
uv run python -m database.import_csv
```

The data will be stored in `hr_database.db` at the project root.

---

# 15. MCP Server

The MCP server does **not** need to be started manually. When the admin agent
initializes (`agent/agent.py` → `mcp_client/client.py`), it automatically
launches `mcp_server/server.py` as a subprocess over stdio and discovers its
tools. You only need `ui/app.py` running (see next step).

---

# 16. Run the Application

Start Streamlit:

```bash
uv run streamlit run ui/app.py
```

The application opens at:

```
http://localhost:8501
```

Log in with any username/password and pick a role (`user` or `admin`) —
authentication is currently a placeholder, not a real credential check
(see Section 21).

---

# 17. MCP Architecture Explanation

```
Admin LangChain Agent
        |
   MCP Client (spawns subprocess, stdio transport)
        |
   MCP Server (FastMCP)
        |
 database/ + actions/ (data access layer)
        |
 SQLite Database
```

The agent never touches the database directly. Instead:

1. The agent decides a tool is required.
2. The MCP client sends a request to the MCP server process.
3. The MCP server executes the corresponding Python function.
4. The database operation is performed.
5. The result is returned to the agent.
6. The LLM generates the final natural-language answer.

---

# 18. Available Tools

## RAG Tool (native LangChain tool — used by both roles)

### `search_hr_policy()`
Searches HR documents in ChromaDB.

```
How many casual leaves are allowed?
```

---

## MCP Tools (admin only, 5 total)

### `get_employee_details(employee_id)`
Retrieves an employee's basic details.
```
Show employee 101 details.
```

### `get_leave_balance(employee_id)`
Retrieves an employee's leave balance.
```
How many leaves does employee 101 have?
```

### `apply_leave(employee_id, leave_type, start_date, end_date, reason)`
Submits a leave request (status defaults to "Pending").
```
Apply sick leave for employee 101 from 2026-08-10 to 2026-08-12, reason: fever.
```

### `raise_hr_ticket(employee_id, subject, description)`
Creates an HR support ticket (status defaults to "Open").
```
Raise a ticket for employee 101 about a payroll issue.
```

### `update_employee_email(employee_id, new_email)`
Updates an employee's email address.
```
Update employee 101's email to new.email@company.com
```

The admin agent has **6 tools total**: the 5 MCP tools above, plus the native `search_hr_policy` RAG tool.

---

# 19. Role Permissions

| Feature                     | User | Admin |
| ---------------------------- | ---- | ----- |
| HR Document Search / Policy Q&A | Yes  | Yes   |
| Employee Details Lookup      | No   | Yes   |
| Leave Balance Lookup         | No   | Yes   |
| Apply Leave                  | No   | Yes   |
| Raise HR Ticket              | No   | Yes   |
| Update Employee Email        | No   | Yes   |

---

# 20. Provider Architecture

The project separates AI providers from application logic via `providers/`.

Current:

```
LangChain
    |
Ollama (local)
```

Future (already supported in `config.py` / provider files, needs credentials):

```
LangChain
    |
Azure OpenAI
```

Switching providers only requires changing `.env` — no application code changes.

---

# 21. Known Limitations

* **Login is not real authentication.** Any non-empty username/password logs
  you in as whichever role is selected from the dropdown — there's no
  credential check or per-employee identity binding.
* **No access control on `employee_id`.** An admin can query or modify any
  employee's record by ID; there's no check tying the logged-in admin to a
  specific employee or permission scope.
* `agent/tools.py` defines `employee_tool` and `hr_action_tool` as native
  LangChain tools, but they are currently unused — the admin agent uses the
  MCP-based equivalents instead.
* `security/roles.py` (`UserRole` enum) is defined but not currently used
  anywhere in the codebase.

---

# 22. Troubleshooting

## Ollama Connection Error

Check installed models:

```bash
ollama list
```

Make sure the Ollama service is running:

```bash
ollama serve
```

## "No such table" errors

Run the database initialization step (Section 14) before importing CSVs or
starting the app.

---

# 23. Future Improvements

* Real authentication system
* JWT-based or session-based security
* Per-employee access scoping (not just role-based)
* Self-service leave/ticket actions for regular users
* Cloud model integration (Azure)
* Monitoring and logging
* Conversation memory

---

# 24. Conclusion

The HR Assistant AI Agent demonstrates an enterprise-style AI architecture combining:

* Retrieval-Augmented Generation
* Local LLM inference via Ollama
* Vector search with ChromaDB
* Structured database access via SQLite
* MCP-based tool execution
* Role-based feature separation

The modular provider layer allows the system to run entirely locally today
while remaining ready for a future cloud AI migration.
