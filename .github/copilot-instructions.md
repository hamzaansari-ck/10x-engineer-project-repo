# PromptLab — AI Coding Agent Instructions

## Project Overview

PromptLab is a FastAPI-based prompt management platform. The backend uses
Pydantic v2 models and an in-memory storage layer. A React + Vite frontend
will be added later.

## Coding Standards

- Python 3.10+ with type hints on all function signatures.
- Use Google-style docstrings on every public function and class.
- Keep functions under 20 lines where possible.
- Use `Optional[X]` for nullable types (not `X | None`) for Pydantic compat.

## File Naming

- Python modules: `snake_case.py`
- Test files: `test_<module>.py` inside `backend/tests/`
- React components (future): `PascalCase.jsx` inside `frontend/src/components/`

## Error Handling

- Use `HTTPException` from FastAPI for all API errors.
- Always return proper status codes: 400 for bad input, 404 for not found, 422 for validation.
- Never let unhandled exceptions reach the client as 500s.

## Testing

- Use `pytest` with the `TestClient` from FastAPI.
- Every new endpoint or feature must have tests covering happy path, error cases, and edge cases.
- Use fixtures from `conftest.py` for shared test data.
- Target 80%+ code coverage.

## Patterns

- Models go in `app/models.py`, routes in `app/api.py`, helpers in `app/utils.py`.
- Storage is abstracted behind `app/storage.py`. Do not access `_prompts` or `_collections` dicts directly outside that module.
- Use `model_dump()` and `model_copy()` (Pydantic v2) instead of `.dict()` / `.copy()`.
- For partial updates use `model_dump(exclude_unset=True)`.

## Commit Messages

- Use conventional commits: `fix:`, `feat:`, `docs:`, `test:`, `chore:`.
- Keep the subject line under 72 characters.

## Dependencies

- Add new Python packages to `backend/requirements.txt`.
- Add new JS packages via `npm install` inside `frontend/`.
