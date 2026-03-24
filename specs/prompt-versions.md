# Feature Spec: Prompt Version History

## Overview

Track every change made to a prompt so users can view previous versions,
compare differences, and restore an older version if needed.

## User Stories

### US-1: Automatic version creation
As a user, when I update a prompt (PUT or PATCH), a new version record is
created automatically so I never lose previous content.

Acceptance criteria:
- A version snapshot is saved before the update is applied.
- The version includes the full prompt content, title, and description.
- The version is timestamped.

### US-2: View version history
As a user, I can view the list of all versions for a prompt so I can see
how it evolved over time.

Acceptance criteria:
- Versions are returned newest-first.
- Each entry shows version number, timestamp, and a summary of changes.

### US-3: View a specific version
As a user, I can view the full content of any past version.

### US-4: Restore a version
As a user, I can restore a prompt to a previous version, which creates a
new version (non-destructive).

## Data Model Changes

New model `PromptVersion`:

```python
class PromptVersion(BaseModel):
    id: str                  # UUID
    prompt_id: str           # FK to Prompt
    version_number: int      # Auto-incrementing per prompt
    title: str
    content: str
    description: Optional[str]
    created_at: datetime     # When this version was saved
```

Storage adds `_prompt_versions: Dict[str, List[PromptVersion]]` keyed by
`prompt_id`.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/prompts/{id}/versions` | List all versions for a prompt |
| GET | `/prompts/{id}/versions/{version_number}` | Get a specific version |
| POST | `/prompts/{id}/versions/{version_number}/restore` | Restore prompt to this version |

### GET /prompts/{id}/versions

Response `200`:
```json
{
  "versions": [
    {
      "id": "uuid",
      "prompt_id": "uuid",
      "version_number": 2,
      "title": "Old title",
      "content": "Old content",
      "description": null,
      "created_at": "2025-01-15T10:00:00"
    }
  ],
  "total": 2
}
```

### POST /prompts/{id}/versions/{version_number}/restore

Response `200`: Returns the updated Prompt (now matching the restored version).
A new version record is also created to preserve the pre-restore state.

## Edge Cases

- Restoring the current version is a no-op but still returns 200.
- Deleting a prompt deletes all its versions.
- Version numbers are immutable and never reused.
- First version (number 1) is created when the prompt is first created.
