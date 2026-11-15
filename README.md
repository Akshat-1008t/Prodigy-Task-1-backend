# Prodigy InfoTech - Backend Development Internship

## Task 01: Basic REST API with CRUD Operations

A RESTful API built with **FastAPI** to manage a `User` resource using an in-memory dictionary data store.

### Features
* **CRUD Functionality**: Create, Read, Update, and Delete operations.
* **UUID Identification**: Unique resource identifiers using Python's `uuid.uuid4()`.
* **Input Validation**: Handled via Pydantic (`EmailStr`, string lengths, integer constraints).
* **HTTP Status Codes**: Returns standard responses (`200 OK`, `201 Created`, `204 No Content`, `400 Bad Request`, `404 Not Found`, `422 Unprocessable Entity`).

### Setup & Run
1. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate