# PromptLab

A prompt engineering platform for AI teams to store, organise, and manage
prompt templates. Think "Postman for Prompts."

## Features

- CRUD operations for prompts with full and partial updates (PUT & PATCH)
- Organise prompts into collections
- Search prompts by title or description
- Filter prompts by collection
- Template variable support (`{{variable}}` syntax)
- Automatic timestamp tracking
- Cascade handling on collection deletion

## Prerequisites

- Python 3.10+
- Node.js 18+ (for the frontend, Week 4)
- Git

## Quick Start

```bash
# Clone and enter the project
git clone <your-repo-url>
cd promptlab

# Install backend dependencies
cd backend
pip install -r requirements.txt

# Start the API server
python main.py
```

- API: http://localhost:8000
- Swagger docs: http://localhost:8000/docs

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
│   │   └── test_api.py      # API endpoint tests
│   ├── main.py              # Uvicorn entry point
│   └── requirements.txt
├── docs/
│   └── API_REFERENCE.md     # Full endpoint documentation
├── specs/
│   ├── prompt-versions.md   # Version history feature spec
│   └── tagging-system.md    # Tagging feature spec
├── frontend/                # React app (Week 4)
├── .github/
│   └── copilot-instructions.md  # AI coding agent config
├── PROJECT_BRIEF.md
├── GRADING_RUBRIC.md
└── README.md
```

## API Overview

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| GET | `/prompts` | List prompts (supports `?search=` and `?collection_id=`) |
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

## Tech Stack

- Python 3.10+, FastAPI, Pydantic v2
- pytest for testing
- React + Vite (frontend, coming in Week 4)
- Docker & GitHub Actions (CI/CD, coming in Week 3)

## Contributing

1. Create a feature branch from `main`.
2. Write tests for any new functionality.
3. Ensure all tests pass and coverage stays above 80%.
4. Use conventional commit messages (`feat:`, `fix:`, `docs:`, `test:`).
5. Open a pull request for review.
