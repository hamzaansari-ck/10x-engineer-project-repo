# PromptLab API Reference

Base URL: `http://localhost:8000`

Interactive docs (Swagger UI): `http://localhost:8000/docs`

## Authentication

No authentication is required at this time. All endpoints are publicly accessible.

---

## Health

### GET /health

Returns the service health status.

**Response** `200 OK`

```json
{
  "status": "healthy",
  "version": "0.1.0"
}
```

---

## Prompts

### GET /prompts

List all prompts, sorted newest first.

**Query Parameters**

| Parameter | Type | Description |
|-----------|------|-------------|
| `collection_id` | string (optional) | Filter by collection |
| `search` | string (optional) | Case-insensitive search in title and description |

**Response** `200 OK`

```json
{
  "prompts": [
    {
      "id": "uuid",
      "title": "Code Review Prompt",
      "content": "Review this code:\n\n{{code}}",
      "description": "A prompt for AI code review",
      "collection_id": null,
      "created_at": "2025-01-15T10:30:00",
      "updated_at": "2025-01-15T10:30:00"
    }
  ],
  "total": 1
}
```

---

### GET /prompts/{prompt_id}

Retrieve a single prompt.

**Path Parameters**

| Parameter | Type | Description |
|-----------|------|-------------|
| `prompt_id` | string | UUID of the prompt |

**Response** `200 OK`

```json
{
  "id": "uuid",
  "title": "Code Review Prompt",
  "content": "Review this code:\n\n{{code}}",
  "description": "A prompt for AI code review",
  "collection_id": null,
  "created_at": "2025-01-15T10:30:00",
  "updated_at": "2025-01-15T10:30:00"
}
```

**Error** `404 Not Found`

```json
{ "detail": "Prompt not found" }
```

---

### POST /prompts

Create a new prompt.

**Request Body**

```json
{
  "title": "Code Review Prompt",
  "content": "Review this code:\n\n{{code}}",
  "description": "A prompt for AI code review",
  "collection_id": null
}
```

| Field | Type | Required | Constraints |
|-------|------|----------|-------------|
| `title` | string | yes | 1-200 chars |
| `content` | string | yes | min 1 char |
| `description` | string | no | max 500 chars |
| `collection_id` | string | no | Must reference existing collection |

**Response** `201 Created` — Returns the full Prompt object.

**Error** `400 Bad Request` — If `collection_id` references a non-existent collection.

**Error** `422 Unprocessable Entity` — If validation fails.

---

### PUT /prompts/{prompt_id}

Fully replace a prompt. All fields are required.

**Request Body** — Same schema as POST.

**Response** `200 OK` — Returns the updated Prompt. `updated_at` is refreshed.

**Error** `404 Not Found` — Prompt does not exist.

**Error** `400 Bad Request` — Invalid `collection_id`.

---

### PATCH /prompts/{prompt_id}

Partially update a prompt. Only provided fields are changed.

**Request Body**

```json
{
  "title": "New Title"
}
```

All fields are optional. Only include the fields you want to change.

**Response** `200 OK` — Returns the updated Prompt. `updated_at` is refreshed.

**Error** `404 Not Found` — Prompt does not exist.

**Error** `400 Bad Request` — Invalid `collection_id`.

---

### DELETE /prompts/{prompt_id}

Delete a prompt.

**Response** `204 No Content`

**Error** `404 Not Found`

---

## Collections

### GET /collections

List all collections.

**Response** `200 OK`

```json
{
  "collections": [
    {
      "id": "uuid",
      "name": "Development",
      "description": "Prompts for development tasks",
      "created_at": "2025-01-15T10:30:00"
    }
  ],
  "total": 1
}
```

---

### GET /collections/{collection_id}

Retrieve a single collection.

**Response** `200 OK` — Returns the Collection object.

**Error** `404 Not Found`

---

### POST /collections

Create a new collection.

**Request Body**

```json
{
  "name": "Development",
  "description": "Prompts for development tasks"
}
```

| Field | Type | Required | Constraints |
|-------|------|----------|-------------|
| `name` | string | yes | 1-100 chars |
| `description` | string | no | max 500 chars |

**Response** `201 Created` — Returns the full Collection object.

---

### DELETE /collections/{collection_id}

Delete a collection. Prompts belonging to the collection are not deleted;
their `collection_id` is set to `null`.

**Response** `204 No Content`

**Error** `404 Not Found`

---

## Error Format

All errors follow this structure:

```json
{
  "detail": "Human-readable error message"
}
```

| Status Code | Meaning |
|-------------|---------|
| 400 | Bad request / validation error |
| 404 | Resource not found |
| 422 | Request body validation failure (Pydantic) |
| 500 | Internal server error |
