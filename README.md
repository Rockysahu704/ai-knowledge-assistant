
# AI Knowledge Assistant

An AI-powered employee policy assistant built with **FastAPI, LangGraph, Groq, PostgreSQL, and Psycopg**.

The application accepts an employee's natural-language question, identifies the relevant policy category, retrieves the corresponding information from PostgreSQL, and uses a Groq LLM to generate a grounded response.

---

## 📌 Project Overview

The AI Knowledge Assistant is designed to answer questions related to employee policies such as:

- Annual Leave
- Vacation
- Holidays

Instead of allowing the LLM to generate answers from its own knowledge, the application retrieves relevant information from PostgreSQL and provides that information as context to the LLM.

This helps keep the generated response grounded in the application's stored policy data.

---

## 🏗️ Current Architecture

```text
                         User
                           │
                           ▼
                    FastAPI REST API
                           │
                           ▼
                      Service Layer
                           │
                           ▼
                       LangGraph
                           │
                 ┌─────────┴─────────┐
                 │                   │
                 ▼                   ▼
       Deterministic Rules      Groq Classifier
                 │                   │
                 └─────────┬─────────┘
                           │
                         Intent
                           │
                           ▼
                    Repository Layer
                           │
                           ▼
                      PostgreSQL
                           │
                           ▼
                        Context
                           │
                           ▼
                   Groq Answer Generator
                           │
                           ▼
                     Final Response
````

---

# 🚀 Features

### 1. FastAPI REST API

Provides an HTTP API for asking employee policy questions.

Example endpoint:

```text
POST /api/ask/
```

---

### 2. Request Validation with Pydantic

Incoming requests are validated using Pydantic models.

Example request:

```json
{
  "question": "How many annual leave days do employees get?"
}
```

Invalid or missing fields are automatically rejected by FastAPI with a validation response.

---

### 3. LangGraph Workflow

LangGraph is used to orchestrate the application's AI workflow.

Current workflow:

```text
START
  ↓
classify_question
  ↓
retrieve_data
  ↓
generate_answer
  ↓
END
```

Each node performs a specific task.

---

### 4. Hybrid Question Classification

The application uses two classification approaches.

#### Deterministic classification

For obvious questions, Python rules are used first.

For example:

```text
"How many annual leave days do employees get?"
```

is directly classified as:

```text
annual_leave
```

This avoids an unnecessary LLM call.

#### Groq fallback classification

If the Python rules cannot identify the question, the application sends the question to Groq.

For example:

```text
"How many paid days off can I take?"
```

The question does not contain the exact phrase `annual leave`, but the LLM can understand that it belongs to:

```text
annual_leave
```

The supported intents are:

```text
annual_leave
vacation
holiday
unknown
```

---

### 5. PostgreSQL Database

Policy information is stored in PostgreSQL.

Current table:

```text
policies
```

The table contains:

* `id`
* `topic`
* `content`

Example data:

```text
annual_leave
Employees receive 20 days of annual leave.

vacation
Employees receive 20 days of vacation.

holiday
Employees receive 20 days of holiday.
```

---

### 6. Repository Layer

Database operations are separated from the LangGraph workflow.

The repository is responsible for retrieving policy information from PostgreSQL.

Example:

```python
get_policy(topic)
```

This keeps database logic separate from application and workflow logic.

---

### 7. Grounded LLM Answer Generation

After retrieving information from PostgreSQL, the context is provided to the Groq LLM.

Conceptually:

```text
User Question
      +
Database Context
      ↓
     Groq
      ↓
Final Answer
```

The prompt instructs the LLM to use only the supplied context and avoid inventing information.

For example:

**Question:**

```text
How many paid days off can I take?
```

**Database context:**

```text
Employees receive 20 days of annual leave.
```

**Generated response:**

```text
Employees are entitled to 20 days of paid annual leave.
```

---

# 📂 Project Structure

```text
ai-knowledge-assistant/
│
├── app/
│   │
│   ├── main.py
│   │
│   ├── routes/
│   │   ├── __init__.py
│   │   └── ask.py
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── ask.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   └── ask_service.py
│   │
│   ├── graph/
│   │   ├── __init__.py
│   │   └── ask_graph.py
│   │
│   ├── llm/
│   │   ├── __init__.py
│   │   ├── classifier.py
│   │   ├── classifier_test.py
│   │   └── answer_generator.py
│   │
│   ├── repositories/
│   │   ├── __init__.py
│   │   └── policy_repository.py
│   │
│   └── database/
│       ├── __init__.py
│       └── connection.py
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

---

# 🧩 Component Responsibilities

| Component                           | Responsibility                                  |
| ----------------------------------- | ----------------------------------------------- |
| `main.py`                           | Creates the FastAPI application                 |
| `routes/ask.py`                     | Defines the API endpoint                        |
| `schemas/ask.py`                    | Defines request and response models             |
| `services/ask_service.py`           | Coordinates the application workflow            |
| `graph/ask_graph.py`                | Defines and orchestrates the LangGraph workflow |
| `llm/classifier.py`                 | Performs LLM-based question classification      |
| `llm/answer_generator.py`           | Generates the final response using Groq         |
| `repositories/policy_repository.py` | Retrieves policy data from PostgreSQL           |
| `database/connection.py`            | Creates the PostgreSQL connection               |

---

# 🛠️ Technologies Used

### Backend

* Python
* FastAPI
* Pydantic
* Uvicorn

### AI / LLM

* LangChain
* LangGraph
* Groq
* `langchain-groq`

### Database

* PostgreSQL
* Psycopg 3

### Configuration

* python-dotenv
* `.env`

---

# ⚙️ Prerequisites

Before running the project, install:

* Python 3.10+
* PostgreSQL
* Git
* A Groq API key

---

# 📥 Installation

## 1. Clone the repository

```bash
git clone <your-repository-url>
```

Move into the project:

```bash
cd ai-knowledge-assistant
```

---

## 2. Create a virtual environment

Windows:

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

You should see something similar to:

```text
(venv)
```

in your terminal.

---

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

If `requirements.txt` has not been created yet, the main packages used by the project are:

```text
fastapi
uvicorn
pydantic
langgraph
langchain
langchain-groq
psycopg[binary]
python-dotenv
typing-extensions
```

---

# 🔐 Environment Variables

Create a `.env` file in the project root.

```env
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_NAME=ai_knowledge_assistant
DATABASE_USER=postgres
DATABASE_PASSWORD=your_postgres_password

GROQ_API_KEY=your_groq_api_key
```

### Important

Do not commit `.env` to GitHub.

Add the following to `.gitignore`:

```text
.env
__pycache__/
venv/
```

---

# 🗄️ Database Setup

Open PostgreSQL / pgAdmin and create the database:

```sql
CREATE DATABASE ai_knowledge_assistant;
```

Connect to the database and create the `policies` table:

```sql
CREATE TABLE policies (
    id SERIAL PRIMARY KEY,
    topic VARCHAR(100) NOT NULL,
    content TEXT NOT NULL
);
```

Insert sample policy data:

```sql
INSERT INTO policies (topic, content)
VALUES
(
    'annual_leave',
    'Employees receive 20 days of annual leave.'
),
(
    'vacation',
    'Employees receive 20 days of vacation.'
),
(
    'holiday',
    'Employees receive 20 days of holiday.'
);
```

Verify the data:

```sql
SELECT * FROM policies;
```

---

# ▶️ Running the Application

From the **project root directory**, start FastAPI:

```bash
uvicorn app.main:app --reload
```

The server will start at:

```text
http://127.0.0.1:8000
```

---

# 📖 API Documentation

FastAPI automatically provides interactive API documentation.

Open:

```text
http://127.0.0.1:8000/docs
```

You can test the API directly using Swagger UI.

Alternative documentation:

```text
http://127.0.0.1:8000/redoc
```

---

# 🔌 API Usage

## Ask a Question

### Endpoint

```text
POST /api/ask/
```

### Request

```json
{
  "question": "How many annual leave days do employees get?"
}
```

### Response

```json
{
  "answer": "Employees receive 20 days of annual leave."
}
```

---

## Example: Natural Language Question

### Request

```json
{
  "question": "How many paid days off can I take?"
}
```

The deterministic classifier does not find the exact phrase `annual leave`.

The question is therefore sent to the Groq classifier.

Groq classifies it as:

```text
annual_leave
```

The application retrieves the corresponding policy from PostgreSQL and generates the answer.

Example response:

```json
{
  "answer": "Employees are entitled to 20 days of paid annual leave."
}
```

---

## Example: Vacation

### Request

```json
{
  "question": "What is the vacation policy?"
}
```

### Response

```json
{
  "answer": "The vacation policy provides employees with 20 days of vacation."
}
```

---

## Example: Unsupported Question

### Request

```json
{
  "question": "What is my name?"
}
```

The application does not have information about the user's name.

The LLM is instructed not to invent an answer.

Example response:

```json
{
  "answer": "I don't have enough information to determine your name."
}
```

---

# 🔄 End-to-End Request Flow

When a user sends:

```text
How many paid days off can I take?
```

the request flows through the application as follows:

### 1. FastAPI receives the request

```text
POST /api/ask/
```

↓

### 2. Pydantic validates the request

```json
{
  "question": "How many paid days off can I take?"
}
```

↓

### 3. Service layer receives the request

The service invokes the LangGraph workflow.

↓

### 4. LangGraph starts

```text
START
```

↓

### 5. Question classification

The deterministic rules are checked first.

No exact match is found.

↓

### 6. Groq fallback classifier

Groq determines:

```text
annual_leave
```

↓

### 7. Retrieve policy

The repository queries PostgreSQL:

```sql
SELECT content
FROM policies
WHERE topic = %s;
```

↓

### 8. PostgreSQL returns context

```text
Employees receive 20 days of annual leave.
```

↓

### 9. Answer generation

The question and database context are sent to Groq.

↓

### 10. Final response

```json
{
  "answer": "Employees are entitled to 20 days of paid annual leave."
}
```

---

# 🧠 Why Use LangGraph?

The current application could technically be implemented using normal Python functions.

LangGraph is being used to explicitly represent the workflow as a graph.

```text
START
  ↓
Classify
  ↓
Retrieve
  ↓
Generate
  ↓
END
```

This becomes especially useful as the application grows and requires:

* Conditional routing
* Multiple tools
* Multiple retrieval steps
* Human approval
* State management
* Retry logic
* Agentic workflows

---

# 🔒 Grounding and Hallucination Control

The application follows a simple grounding strategy.

The LLM receives:

```text
Question
+
Retrieved database context
```

The prompt instructs the model to answer using the provided context.

If sufficient information is not available, the model is instructed to say that it does not have enough information.

This prevents the assistant from intentionally filling missing policy information with unsupported answers.

---

# 🧪 Testing

The LLM classifier can be tested independently:

```bash
python -m app.llm.classifier_test
```

Example:

```text
Question: How many paid days off can I take?
Intent: annual_leave
```

The complete API can be tested through:

```text
http://127.0.0.1:8000/docs
```

---

# 📌 Current Limitations

This is the **initial backend implementation**.

Current limitations include:

* Only a small number of policy categories are supported.
* Policy data is currently stored as simple records in PostgreSQL.
* Classification still uses a combination of deterministic rules and LLM fallback.
* LLM classification currently relies on the model returning one of the expected intent names.
* Authentication and authorization are not implemented.
* Conversation history is not implemented.
* Vector search / semantic retrieval is not implemented yet.
* LangSmith tracing is not implemented yet.
* React frontend is not implemented yet.
* Azure deployment is not implemented yet.

---

# 🚧 Future Improvements

Planned improvements include:

### Phase 1 — Backend Improvements

* Structured LLM outputs
* Better intent classification
* More policy categories
* Improved error handling
* Database connection management
* Automated tests
* Logging

### Phase 2 — RAG

Introduce:

```text
PostgreSQL
    +
pgvector
    ↓
Vector Search
    ↓
Relevant Documents
    ↓
LLM
```

This will allow the assistant to retrieve semantically relevant policy information rather than relying only on exact topic classification.

### Phase 3 — LangSmith

Add LangSmith for:

* LLM tracing
* Debugging
* Prompt monitoring
* Token usage monitoring
* LangGraph execution tracing
* Evaluation

### Phase 4 — Frontend

Build a React frontend using:

```text
Vite
React
```

The frontend will communicate with the FastAPI backend.

```text
React
  ↓
FastAPI
  ↓
LangGraph
  ↓
PostgreSQL + Groq
```

### Phase 5 — Azure Deployment

Deploy the application to Microsoft Azure.

Potential architecture:

```text
React Frontend
      ↓
Azure
      ↓
FastAPI Backend
      ↓
PostgreSQL
      ↓
Groq API
```

---

# 📚 Learning Objectives

This project was developed to understand how different backend and AI components work together in a real application.

Key concepts practiced:

* REST API development
* FastAPI routing
* Pydantic validation
* Service-layer architecture
* Repository pattern
* PostgreSQL integration
* Psycopg
* Environment variables
* LangGraph state and nodes
* LLM-based classification
* Hybrid AI workflows
* Grounded LLM generation
* API testing with Swagger UI

---

# 👨‍💻 Author

**Rocky Sahu**

Python Full Stack Developer

### Technologies of Interest

* Python
* Django
* FastAPI
* React.js
* LangChain
* LangGraph
* Generative AI
* PostgreSQL
* REST APIs

---

# ⭐ Project Status

**Backend Phase: Completed**

Current working stack:

```text
Python
   │
FastAPI
   │
LangGraph
   │
Groq
   │
PostgreSQL
```

Future phases:

```text
RAG / PGVector
      ↓
LangSmith
      ↓
React + Vite
      ↓
Azure Deployment
```

```


