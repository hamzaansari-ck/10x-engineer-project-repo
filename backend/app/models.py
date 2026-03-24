"""Pydantic models for PromptLab.

This module defines all data models used throughout the PromptLab application,
including request/response schemas for prompts, collections, and API responses.
All models use Pydantic v2 for validation and serialization.
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from uuid import uuid4


def generate_id() -> str:
    """Generate a unique identifier for a new resource.

    Returns:
        A UUID4 string to be used as a primary key.

    Example:
        >>> id_val = generate_id()
        >>> len(id_val) == 36
        True
    """
    return str(uuid4())


def get_current_time() -> datetime:
    """Return the current UTC timestamp.

    Returns:
        A timezone-naive datetime representing the current UTC time.

    Example:
        >>> ts = get_current_time()
        >>> isinstance(ts, datetime)
        True
    """
    return datetime.utcnow()


# ============== Prompt Models ==============

class PromptBase(BaseModel):
    """Base schema shared by all prompt-related models.

    Attributes:
        title: The prompt title. Must be between 1 and 200 characters.
        content: The prompt template body. Supports ``{{variable}}`` placeholders.
        description: An optional short description (max 500 chars).
        collection_id: Optional ID linking this prompt to a collection.
        tags: List of tag labels attached to this prompt.
    """

    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1)
    description: Optional[str] = Field(None, max_length=500)
    collection_id: Optional[str] = None
    tags: List[str] = Field(default_factory=list)


class PromptCreate(PromptBase):
    """Schema for creating a new prompt.

    Inherits all fields from PromptBase. All base fields are required
    except ``description`` and ``collection_id`` which remain optional.
    """

    pass


class PromptUpdate(PromptBase):
    """Schema for fully updating an existing prompt (PUT).

    All base fields must be provided. This performs a complete replacement
    of the prompt's mutable fields.
    """

    pass


class PromptPatch(BaseModel):
    """Schema for partially updating an existing prompt (PATCH).

    All fields are optional. Only fields included in the request body
    will be updated; omitted fields remain unchanged.

    Attributes:
        title: New title for the prompt (1-200 chars).
        content: New prompt body (min 1 char).
        description: New description (max 500 chars).
        collection_id: New collection association, or None to remove.
    """

    title: Optional[str] = Field(None, min_length=1, max_length=200)
    content: Optional[str] = Field(None, min_length=1)
    description: Optional[str] = Field(None, max_length=500)
    collection_id: Optional[str] = None
    tags: Optional[List[str]] = None


class Prompt(PromptBase):
    """Full prompt model returned by the API.

    Extends PromptBase with server-generated fields for identity and timestamps.

    Attributes:
        id: Unique identifier (UUID4), auto-generated on creation.
        created_at: UTC timestamp of when the prompt was created.
        updated_at: UTC timestamp of the last modification.
    """

    id: str = Field(default_factory=generate_id)
    created_at: datetime = Field(default_factory=get_current_time)
    updated_at: datetime = Field(default_factory=get_current_time)

    class Config:
        """Pydantic configuration for Prompt model."""

        from_attributes = True


# ============== Collection Models ==============

class CollectionBase(BaseModel):
    """Base schema shared by all collection-related models.

    Attributes:
        name: The collection name. Must be between 1 and 100 characters.
        description: An optional short description (max 500 chars).
    """

    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)


class CollectionCreate(CollectionBase):
    """Schema for creating a new collection.

    Inherits all fields from CollectionBase.
    """

    pass


class Collection(CollectionBase):
    """Full collection model returned by the API.

    Attributes:
        id: Unique identifier (UUID4), auto-generated on creation.
        created_at: UTC timestamp of when the collection was created.
    """

    id: str = Field(default_factory=generate_id)
    created_at: datetime = Field(default_factory=get_current_time)

    class Config:
        """Pydantic configuration for Collection model."""

        from_attributes = True


# ============== Response Models ==============

class PromptList(BaseModel):
    """Paginated list response for prompts.

    Attributes:
        prompts: List of Prompt objects matching the query.
        total: Total number of prompts in the result set.
    """

    prompts: List[Prompt]
    total: int


class CollectionList(BaseModel):
    """Paginated list response for collections.

    Attributes:
        collections: List of Collection objects.
        total: Total number of collections in the result set.
    """

    collections: List[Collection]
    total: int


class HealthResponse(BaseModel):
    """Health check response model.

    Attributes:
        status: Service health status string (e.g. ``"healthy"``).
        version: Current application version.
    """

    status: str
    version: str


class TagCount(BaseModel):
    """A single tag with its usage count.

    Attributes:
        name: The normalised tag string.
        count: Number of prompts using this tag.
    """

    name: str
    count: int


class TagList(BaseModel):
    """Response model for the tags endpoint.

    Attributes:
        tags: List of TagCount objects sorted by count descending.
    """

    tags: List[TagCount]
