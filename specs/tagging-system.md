# Feature Spec: Tagging System

## Overview

Allow users to attach tags to prompts for flexible categorisation and
discovery. Tags are lightweight labels (e.g. "python", "code-review",
"marketing") that complement the collection hierarchy.

## User Stories

### US-1: Add tags when creating a prompt
As a user, I can provide a list of tags when creating or updating a prompt.

Acceptance criteria:
- Tags are an optional list of strings on the prompt model.
- Tags are stored lowercase and trimmed of whitespace.
- Duplicate tags on the same prompt are silently ignored.

### US-2: Filter prompts by tag
As a user, I can filter the prompt list by one or more tags so I can
quickly find related prompts.

Acceptance criteria:
- `GET /prompts?tag=python` returns only prompts tagged "python".
- Multiple tags can be provided: `?tag=python&tag=review` (AND logic).

### US-3: List all tags
As a user, I can see all tags in use across the system with prompt counts.

### US-4: Remove a tag
As a user, I can remove a tag from a prompt via PATCH.

## Data Model Changes

Add `tags` field to prompt models:

```python
class PromptBase(BaseModel):
    title: str
    content: str
    description: Optional[str] = None
    collection_id: Optional[str] = None
    tags: List[str] = Field(default_factory=list)  # NEW
```

Tags are normalised on write: lowercased, stripped, deduplicated.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/prompts?tag=python` | Filter prompts by tag(s) |
| GET | `/tags` | List all unique tags with counts |

### GET /tags

Response `200`:
```json
{
  "tags": [
    { "name": "python", "count": 12 },
    { "name": "code-review", "count": 5 }
  ]
}
```

### Filtering

`GET /prompts?tag=python&tag=review` returns prompts that have both tags
(AND logic). Combined with existing `search` and `collection_id` filters.

## Implementation Notes

- Add a `filter_prompts_by_tags(prompts, tags)` helper in `utils.py`.
- Tag normalisation helper: `normalise_tags(tags: List[str]) -> List[str]`.
- Storage does not need a separate tags table; tags live on the Prompt model.

## Edge Cases

- Empty string tags are rejected (validation error).
- Tag names max 50 characters.
- A prompt can have at most 20 tags.
- Deleting a prompt removes its tags implicitly.
- Tags with only whitespace are rejected.
