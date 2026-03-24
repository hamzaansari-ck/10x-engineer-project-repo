"""Model validation tests for PromptLab."""

import pytest
from pydantic import ValidationError
from app.models import (
    Prompt, PromptCreate, PromptUpdate, PromptPatch,
    Collection, CollectionCreate,
    PromptList, CollectionList, HealthResponse,
    generate_id, get_current_time,
)


class TestGenerateId:
    """Tests for the generate_id helper."""

    def test_returns_string(self):
        assert isinstance(generate_id(), str)

    def test_unique(self):
        assert generate_id() != generate_id()

    def test_uuid_format(self):
        id_val = generate_id()
        assert len(id_val) == 36
        assert id_val.count("-") == 4


class TestGetCurrentTime:
    """Tests for the get_current_time helper."""

    def test_returns_datetime(self):
        from datetime import datetime
        assert isinstance(get_current_time(), datetime)


class TestPromptCreate:
    """Tests for PromptCreate validation."""

    def test_valid_minimal(self):
        p = PromptCreate(title="T", content="C")
        assert p.title == "T"
        assert p.description is None
        assert p.collection_id is None
        assert p.tags == []

    def test_valid_full(self):
        p = PromptCreate(
            title="Title", content="Body", description="Desc",
            collection_id="col-1", tags=["python", "ai"]
        )
        assert p.tags == ["python", "ai"]

    def test_empty_title_rejected(self):
        with pytest.raises(ValidationError):
            PromptCreate(title="", content="C")

    def test_title_too_long(self):
        with pytest.raises(ValidationError):
            PromptCreate(title="x" * 201, content="C")

    def test_empty_content_rejected(self):
        with pytest.raises(ValidationError):
            PromptCreate(title="T", content="")


class TestPromptPatch:
    """Tests for PromptPatch validation."""

    def test_all_optional(self):
        p = PromptPatch()
        assert p.title is None
        assert p.content is None

    def test_partial_fields(self):
        p = PromptPatch(title="New")
        assert p.title == "New"
        assert p.content is None

    def test_tags_patch(self):
        p = PromptPatch(tags=["new-tag"])
        assert p.tags == ["new-tag"]


class TestPrompt:
    """Tests for the full Prompt model."""

    def test_defaults_generated(self):
        p = Prompt(title="T", content="C")
        assert p.id is not None
        assert p.created_at is not None
        assert p.updated_at is not None
        assert p.tags == []

    def test_serialization(self):
        p = Prompt(title="T", content="C", tags=["a", "b"])
        data = p.model_dump()
        assert "id" in data
        assert "created_at" in data
        assert data["tags"] == ["a", "b"]


class TestCollection:
    """Tests for Collection models."""

    def test_create_valid(self):
        c = CollectionCreate(name="Dev")
        assert c.name == "Dev"

    def test_empty_name_rejected(self):
        with pytest.raises(ValidationError):
            CollectionCreate(name="")

    def test_name_too_long(self):
        with pytest.raises(ValidationError):
            CollectionCreate(name="x" * 101)

    def test_defaults(self):
        c = Collection(name="Dev")
        assert c.id is not None
        assert c.created_at is not None


class TestResponseModels:
    """Tests for response wrapper models."""

    def test_prompt_list(self):
        pl = PromptList(prompts=[], total=0)
        assert pl.total == 0

    def test_collection_list(self):
        cl = CollectionList(collections=[], total=0)
        assert cl.total == 0

    def test_health_response(self):
        h = HealthResponse(status="healthy", version="0.1.0")
        assert h.status == "healthy"
