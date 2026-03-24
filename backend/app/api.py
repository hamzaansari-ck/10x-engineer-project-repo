"""FastAPI routes for PromptLab.

This module defines all HTTP endpoints for the PromptLab API, including
CRUD operations for prompts and collections, health checks, and query
filtering/sorting capabilities.
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional

from app.models import (
    Prompt, PromptCreate, PromptUpdate, PromptPatch,
    Collection, CollectionCreate,
    PromptList, CollectionList, HealthResponse,
    TagList, TagCount,
    get_current_time
)
from app.storage import storage
from app.utils import (
    sort_prompts_by_date, filter_prompts_by_collection,
    search_prompts, normalise_tags, filter_prompts_by_tags,
)
from app import __version__


app = FastAPI(
    title="PromptLab API",
    description="AI Prompt Engineering Platform",
    version=__version__
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============== Health Check ==============

@app.get("/health", response_model=HealthResponse)
def health_check():
    """Return the current health status and version of the API.

    Returns:
        HealthResponse with status ``"healthy"`` and the app version.
    """
    return HealthResponse(status="healthy", version=__version__)


# ============== Prompt Endpoints ==============

@app.get("/prompts", response_model=PromptList)
def list_prompts(
    collection_id: Optional[str] = None,
    search: Optional[str] = None,
    tag: Optional[List[str]] = Query(None)
):
    """List all prompts with optional filtering and search.

    Args:
        collection_id: If provided, only return prompts belonging to this collection.
        search: If provided, filter prompts whose title or description contains
            this substring (case-insensitive).
        tag: If provided, only return prompts that have all specified tags (AND logic).

    Returns:
        PromptList containing the matching prompts sorted newest-first and a total count.
    """
    prompts = storage.get_all_prompts()

    if collection_id:
        prompts = filter_prompts_by_collection(prompts, collection_id)

    if search:
        prompts = search_prompts(prompts, search)

    if tag:
        prompts = filter_prompts_by_tags(prompts, tag)

    prompts = sort_prompts_by_date(prompts, descending=True)

    return PromptList(prompts=prompts, total=len(prompts))


@app.get("/prompts/{prompt_id}", response_model=Prompt)
def get_prompt(prompt_id: str):
    """Retrieve a single prompt by its unique identifier.

    Args:
        prompt_id: The UUID of the prompt to retrieve.

    Returns:
        The matching Prompt object.

    Raises:
        HTTPException: 404 if no prompt exists with the given ID.
    """
    prompt = storage.get_prompt(prompt_id)
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")
    return prompt


@app.post("/prompts", response_model=Prompt, status_code=201)
def create_prompt(prompt_data: PromptCreate):
    """Create a new prompt.

    Args:
        prompt_data: The prompt fields to create. If ``collection_id`` is
            provided, the referenced collection must exist.

    Returns:
        The newly created Prompt with generated ``id`` and timestamps.

    Raises:
        HTTPException: 400 if the referenced collection does not exist.
    """
    if prompt_data.collection_id:
        collection = storage.get_collection(prompt_data.collection_id)
        if not collection:
            raise HTTPException(status_code=400, detail="Collection not found")

    data = prompt_data.model_dump()
    data["tags"] = normalise_tags(data.get("tags", []))
    prompt = Prompt(**data)
    return storage.create_prompt(prompt)


@app.put("/prompts/{prompt_id}", response_model=Prompt)
def update_prompt(prompt_id: str, prompt_data: PromptUpdate):
    """Fully replace an existing prompt's mutable fields.

    All fields in ``PromptUpdate`` are required. The ``updated_at`` timestamp
    is automatically set to the current time.

    Args:
        prompt_id: The UUID of the prompt to update.
        prompt_data: Complete set of new field values.

    Returns:
        The updated Prompt object.

    Raises:
        HTTPException: 404 if the prompt does not exist.
        HTTPException: 400 if the referenced collection does not exist.
    """
    existing = storage.get_prompt(prompt_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Prompt not found")

    if prompt_data.collection_id:
        collection = storage.get_collection(prompt_data.collection_id)
        if not collection:
            raise HTTPException(status_code=400, detail="Collection not found")

    updated_prompt = Prompt(
        id=existing.id,
        title=prompt_data.title,
        content=prompt_data.content,
        description=prompt_data.description,
        collection_id=prompt_data.collection_id,
        tags=normalise_tags(prompt_data.tags),
        created_at=existing.created_at,
        updated_at=get_current_time()
    )

    return storage.update_prompt(prompt_id, updated_prompt)


@app.patch("/prompts/{prompt_id}", response_model=Prompt)
def patch_prompt(prompt_id: str, prompt_data: PromptPatch):
    """Partially update an existing prompt.

    Only the fields included in the request body are modified; all other
    fields retain their current values. The ``updated_at`` timestamp is
    automatically refreshed.

    Args:
        prompt_id: The UUID of the prompt to patch.
        prompt_data: A sparse set of fields to update.

    Returns:
        The updated Prompt object.

    Raises:
        HTTPException: 404 if the prompt does not exist.
        HTTPException: 400 if the referenced collection does not exist.
    """
    existing = storage.get_prompt(prompt_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Prompt not found")

    update_fields = prompt_data.model_dump(exclude_unset=True)

    if "collection_id" in update_fields and update_fields["collection_id"]:
        collection = storage.get_collection(update_fields["collection_id"])
        if not collection:
            raise HTTPException(status_code=400, detail="Collection not found")

    if "tags" in update_fields:
        update_fields["tags"] = normalise_tags(update_fields["tags"] or [])

    updated_prompt = existing.model_copy(update=update_fields)
    updated_prompt.updated_at = get_current_time()

    return storage.update_prompt(prompt_id, updated_prompt)


@app.delete("/prompts/{prompt_id}", status_code=204)
def delete_prompt(prompt_id: str):
    """Delete a prompt by its unique identifier.

    Args:
        prompt_id: The UUID of the prompt to delete.

    Returns:
        None (HTTP 204 No Content on success).

    Raises:
        HTTPException: 404 if the prompt does not exist.
    """
    if not storage.delete_prompt(prompt_id):
        raise HTTPException(status_code=404, detail="Prompt not found")
    return None


# ============== Collection Endpoints ==============

@app.get("/collections", response_model=CollectionList)
def list_collections():
    """List all collections.

    Returns:
        CollectionList containing all collections and a total count.
    """
    collections = storage.get_all_collections()
    return CollectionList(collections=collections, total=len(collections))


@app.get("/collections/{collection_id}", response_model=Collection)
def get_collection(collection_id: str):
    """Retrieve a single collection by its unique identifier.

    Args:
        collection_id: The UUID of the collection to retrieve.

    Returns:
        The matching Collection object.

    Raises:
        HTTPException: 404 if no collection exists with the given ID.
    """
    collection = storage.get_collection(collection_id)
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    return collection


@app.post("/collections", response_model=Collection, status_code=201)
def create_collection(collection_data: CollectionCreate):
    """Create a new collection.

    Args:
        collection_data: The collection fields (name, optional description).

    Returns:
        The newly created Collection with generated ``id`` and timestamp.
    """
    collection = Collection(**collection_data.model_dump())
    return storage.create_collection(collection)


@app.delete("/collections/{collection_id}", status_code=204)
def delete_collection(collection_id: str):
    """Delete a collection and disassociate its prompts.

    Any prompts that belonged to the deleted collection will have their
    ``collection_id`` set to ``None`` rather than being deleted.

    Args:
        collection_id: The UUID of the collection to delete.

    Returns:
        None (HTTP 204 No Content on success).

    Raises:
        HTTPException: 404 if the collection does not exist.
    """
    orphaned_prompts = storage.get_prompts_by_collection(collection_id)

    if not storage.delete_collection(collection_id):
        raise HTTPException(status_code=404, detail="Collection not found")

    for prompt in orphaned_prompts:
        prompt.collection_id = None
        storage.update_prompt(prompt.id, prompt)

    return None



# ============== Tag Endpoints ==============

@app.get("/tags", response_model=TagList)
def list_tags():
    """List all unique tags with usage counts, sorted by count descending.

    Returns:
        TagList containing tag names and their prompt counts.
    """
    from collections import Counter

    counter: Counter = Counter()
    for prompt in storage.get_all_prompts():
        counter.update(prompt.tags)

    tags = [TagCount(name=name, count=count) for name, count in counter.most_common()]
    return TagList(tags=tags)
