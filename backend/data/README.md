
# Banking Data Analysis Platform

A learning project for banking analytics using Python, FastAPI, React,
Pandas, Excel, and Retrieval-Augmented Generation (RAG).

## Project Objectives

- Analyze customer and transaction data.
- Monitor loan portfolios and overdue accounts.
- Explore branch and customer performance.
- Validate and normalize banking records.
- Create API endpoints for dashboard data.
- Explore document retrieval using embeddings and FAISS.
- Containerize the frontend and backend with Docker Compose.

## Technology Stack

### Frontend
- React
- Vite
- React Router
- Recharts
- Lucide React
- Nginx

### Backend
- Python
- FastAPI
- Uvicorn
- Pandas
- OpenPyXL

### RAG and AI
- Sentence Transformers
- FAISS
- Google Gemini API (optional, if configured)

### Deployment and DevOps
- Docker
- Docker Compose
- Git and GitHub

## Project Structure

```text
Banking_Data_Analysis/
├── backend/
│   ├── app/
│   │   └── rag/
│   │       ├── documents/
│   │       ├── faiss_index/
│   │       ├── metadata/
│   │       ├── embeddings.py
│   │       ├── vector_store.py
│   │       ├── retriever.py
│   │       └── gemini_service.py
│   ├── data/
│   │   └── Banking_Dataset.xlsx
│   ├── generate_index.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env
├── frontend/
│   ├── src/
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml
└── README.md
```

The structure above is the intended layout. Some files may need to be
created if they do not exist in your local project yet.

## Prerequisites

Install the following:

- Python
- Node.js and npm
- Docker Desktop
- Git (optional, for version control)

## 1. Create the Banking Dataset

From the backend directory, run:

```powershell
cd backend
python create_banking_dataset.py
```

This generates `data/Banking_Dataset.xlsx` if you have created the
dataset-generation script described in the project instructions.

## 2. Run the Backend Locally

From the project root:

```powershell
cd backend
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

Backend API:

http://localhost:8000

Interactive API documentation:

http://localhost:8000/docs

## 3. Run the Frontend Locally

Open a second terminal:

```powershell
cd frontend
npm install
npm run dev
```

Open the Vite URL shown in the terminal, usually:

http://localhost:5173

## 4. Run with Docker Compose

From the project root:

```powershell
docker compose up --build
```

Open the frontend:

http://localhost:8080

Open the backend API documentation:

http://localhost:8000/docs

To stop the containers:

```powershell
docker compose down
```

To rebuild after changing application code:

```powershell
docker compose up --build
```

## 5. RAG Index Generation

After preparing non-empty source documents in the expected JSONL format,
run the index-generation script:

```powershell
cd backend
python generate_index.py
```

The index-generation script, document store, and retrieval service must
use consistent file paths and the same embedding model.

## Environment Variables

Create `backend/.env` locally and configure only the variables your
backend actually uses. For example:

```env
GEMINI_API_KEY=your_rotated_api_key_here
```

Never commit real API keys or credentials to GitHub.

Add `.env` to `.gitignore` and `.dockerignore` where appropriate.
Use environment variables or a secret manager for production deployment.

## Data Privacy and Security

- Use synthetic or anonymized data for development.
- Do not upload real customer banking details or account numbers.
- Validate inputs and enforce authorization before exposing sensitive APIs.
- Treat RAG answers as informational; verify them against source records.
- Do not expose API keys in frontend code.

## Current Project Status

This repository is a development project. Dashboard integrations,
data validation, RAG indexing, API authentication, automated tests,
and production deployment should be verified before production use.

## Future Enhancements

- Add database persistence with MySQL or PostgreSQL.
- Implement API authentication and role-based access control.
- Add transaction and loan analytics endpoints.
- Improve fraud-alert rules and validation.
- Add unit and integration tests.
- Build a CI/CD pipeline using Jenkins.
- Deploy to a cloud environment after security review.

## Disclaimer

The sample banking dataset is synthetic and intended for educational
purposes. This project is not a real banking system and should not be
used to make real credit, fraud, or financial decisions.
