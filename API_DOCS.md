# API Documentation: Document Q&A (RAG) System

This document outlines the available Application Programming Interface (API) endpoints for the Retrieval-Augmented Generation (RAG) system. The API is built using Django REST Framework (DRF) and allows seamless interaction with the uploaded document knowledge base via Large Language Models (LLMs).

## Base URL
Local Development / Docker: `http://localhost:8000`

---

## 1. Ask a Question Endpoint

This is the core endpoint of the RAG system. It receives a user's question, vectorizes it, retrieves the most relevant chunks from the ChromaDB vector store, and generates a context-aware answer using the OpenRouter LLM API.

- **URL:** `/api/ask/`
- **Method:** `POST`
- **Content-Type:** `application/json`

### Headers Required
| Key | Value | Description |
| :--- | :--- | :--- |
| `Content-Type` | `application/json` | Indicates the payload format. |
| `X-CSRFToken` | `<token_string>` | Required for CSRF protection when making requests from the web interface. |

### Request Body
The request must contain a JSON object with a single `question` key.

```json
{
  "question": "What are the health benefits of deep sleep?"
}
```

### Success Response (HTTP 200 OK)
Returns the generated answer along with metadata (source documents and the exact prompt used).

```json
{
  "answer": "Deep sleep is crucial for tissue repair, muscle growth, and strengthening the immune system. It also helps the brain process and consolidate daily information into long-term memory.",
  "sources": [
    "deep_sleep_health.docx"
  ],
  "prompt": "Answer the user's question based only on the following context...\n\nContext: [Extracted Text...]\n\nQuestion: What are the health benefits of deep sleep?"
}
```

### Error Responses

#### HTTP 400 Bad Request
Occurs when the `question` field is missing or empty in the payload.
```json
{
  "error": "Question not provided"
}
```

#### HTTP 500 Internal Server Error
Occurs when there is an issue with the backend, vector database retrieval, or the connection to the external LLM provider.
```json
{
  "error": "Connection error." 
}
```

---

## 2. User Interfaces & Admin Endpoints

In addition to the REST API, the system provides out-of-the-box user interfaces for chat interaction and data management.

### Chat Interface (Frontend)
- **URL:** `/api/chat/`
- **Method:** `GET`
- **Description:** Renders a modern, interactive HTML/JS chat interface where users can ask questions and view the chat history loaded directly from the database.

### Django Admin Panel
- **URL:** `/admin/`
- **Description:** The central hub for managing the system's data. Requires superuser credentials.
- **Key Modules:**
  - **Documents (`/admin/documents/document/`):** Upload (PDF, DOCX, TXT), edit, or delete documents. Note: Deleting a document here will automatically trigger the deletion of its physical file and its orphan vectors inside ChromaDB.
  - **QA History (`/admin/documents/qahistory/`):** View the logs of all user queries, generated answers, associated sources, and timestamps.