# Django RAG System (Document Q&A)

This project is an advanced Retrieval-Augmented Generation (RAG) system built with Django, LangChain, and ChromaDB. It allows users to upload documents and ask natural language questions based on the document contents using LLMs.

## Features
- Supported Formats: .docx, .pdf, .txt
- Vector Database: ChromaDB (Local)
- Embedding Model: paraphrase-multilingual-MiniLM-L12-v2 (Fully offline, stored locally to prevent network timeouts)
- LLM Integration: OpenRouter API (meta-llama/llama-3-8b-instruct or similar)
- UI & API: Full Django Admin panel for document management and a modern Chat UI for Q&A.
- Smart Deletion: Completely removes physical files and orphan vectors from ChromaDB upon document deletion.
- Local Mirrors (DevNeeds): Docker base images and Python packages are fetched securely via `devneeds.ir` to bypass network restrictions and ensure extremely fast and reliable builds.

## Prerequisites
- Docker and Docker Compose installed.
- (Optional but recommended in restricted networks) A VPN/Proxy running on port 10808 to access OpenRouter API.

## Setup & Installation

1. Environment Variables:
Create a .env file in the root directory containing your OpenRouter API key:
`OPENROUTER_API_KEY=sk-or-v1-...`

2. Run with Docker:
Execute the following command in the root directory:
docker compose up --build

* Note: Since the database is fresh, create an admin user to upload documents by running:
docker compose exec web python manage.py createsuperuser

3. Access the Application:
- Chat Interface: http://localhost:8000/api/chat/
- Admin Panel: http://localhost:8000/admin/

## Sample Files
A set of ready-to-use sample documents is provided in the `Sample files` directory. You can upload these via the Django Admin panel to test the RAG system's accuracy and its multilingual understanding capabilities.

## Documentation
- API Documentation can be found in the API_DOCS.md file.

## 💡 Fallback: Offline Model Loading (Network Issues)
If Docker fails to download the HuggingFace embedding model at runtime due to network restrictions or timeout errors, you can download the model manually into the project folder. 

1. Run the provided script on your host machine:
   python fetch_model.py
2. The script will download the model files (~470MB) into a `local_model_files` directory.
3. The system is smartly configured to detect this folder. Restart your Docker container, and it will automatically use the offline model without requiring internet access for embeddings!
