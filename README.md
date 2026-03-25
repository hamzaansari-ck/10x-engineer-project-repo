# PromptLab

A prompt engineering platform for AI teams to store, organise, and manage
prompt templates. Think "Postman for Prompts."

## Features

- CRUD operations for prompts with full and partial updates (PUT & PATCH)
- Organise prompts into collections
- Tagging system with normalisation and filtering
- Search prompts by title or description
- Filter prompts by collection or tags
- Template variable support (`{{variable}}` syntax)
- Automatic timestamp tracking
- Cascade handling on collection deletion
- React frontend with responsive design
- Full-stack CRUD: create, edit, delete prompts and collections from the UI

## Prerequisites

- Python 3.10+
- Node.js 18+ and npm
- Git

## Quick Start

```bash
# Clone and enter the project
git clone <your-repo-url>
cd promptlab

# --- Backend ---
cd backend
pip install -r requirements.txt
python main.py
# API: http://localhost:8000
# Swagger docs: http://localhost:8000/docs

# --- Frontend (new terminal) ---
cd frontend
npm install
npm run dev
# UI: http://localhost:5173
```

### Using Docker

```bash
docker-compose up --build
```

- Backend: http://localhost:8000
- Frontend: http://localhost:5173

## Running Tests

```bash
cd backend
pytest tests/ -v
```

With coverage:

```bash
pytest tests/ -v --cov=app --cov-report=term-missing
```

## Project Structure

```
promptlab/
├── backend/
│   ├── app/
│   │   ├── __init__.py      # Package version
│   │   ├── api.py           # FastAPI route handlers
│   │   ├── models.py        # Pydantic data models
│   │   ├── storage.py       # In-memory storage layer
│   │   └── utils.py         # Sorting, filtering, search helpers
│   ├── tests/
│   │   ├── conftest.py      # Shared fixtures
│   │   ├── test_api.py      # API endpoint tests
│   │   ├── test_models.py   # Model validation tests
│   │   ├── test_storage.py  # Storage layer tests
│   │   └── test_utils.py    # Utility function tests
│   ├── main.py              # Uvicorn entry point
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── api/             # API client layer
│   │   ├── components/      # React components
│   │   ├── App.jsx          # Main application
│   │   ├── index.css        # Global styles
│   │   └── main.jsx         # Entry point
│   ├── package.json
│   └── vite.config.js
├── docs/
│   └── API_REFERENCE.md     # Full endpoint documentation
├── specs/
│   ├── prompt-versions.md   # Version history feature spec
│   └── tagging-system.md    # Tagging feature spec
├── .github/
│   ├── workflows/ci.yml     # GitHub Actions CI pipeline
│   └── copilot-instructions.md  # AI coding agent config
├── docker-compose.yml
├── PROJECT_BRIEF.md
├── GRADING_RUBRIC.md
└── README.md
```

## API Overview

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| GET | `/tags` | List all tags with counts |
| GET | `/prompts` | List prompts (supports `?search=`, `?collection_id=`, `?tag=`) |
| GET | `/prompts/{id}` | Get a single prompt |
| POST | `/prompts` | Create a prompt |
| PUT | `/prompts/{id}` | Full update |
| PATCH | `/prompts/{id}` | Partial update |
| DELETE | `/prompts/{id}` | Delete a prompt |
| GET | `/collections` | List collections |
| GET | `/collections/{id}` | Get a single collection |
| POST | `/collections` | Create a collection |
| DELETE | `/collections/{id}` | Delete a collection (prompts are disassociated) |

See [docs/API_REFERENCE.md](docs/API_REFERENCE.md) for full request/response
examples.

## Development Setup

### Backend

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r backend/requirements.txt
   ```
3. Run the server with hot reload:
   ```bash
   cd backend
   python main.py
   ```

### Frontend

1. Install dependencies:
   ```bash
   cd frontend
   npm install
   ```
2. Start the dev server:
   ```bash
   npm run dev
   ```
3. Build for production:
   ```bash
   npm run build
   ```

The Vite dev server proxies `/api` requests to the backend at `http://localhost:8000`.

## Tech Stack

- Python 3.10+, FastAPI, Pydantic v2
- pytest (113 tests, 100% coverage)
- React 18 + Vite 5
- Docker & GitHub Actions CI/CD

## Contributing

1. Create a feature branch from `main`.
2. Write tests for any new functionality.
3. Ensure all tests pass and coverage stays above 80%.
4. Use conventional commit messages (`feat:`, `fix:`, `docs:`, `test:`).
5. Open a pull request for review.
