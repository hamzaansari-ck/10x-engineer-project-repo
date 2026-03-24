"""Utility function tests for PromptLab."""

from app.models import Prompt
from app.utils import (
    sort_prompts_by_date,
    filter_prompts_by_collection,
    search_prompts,
    validate_prompt_content,
    extract_variables,
    normalise_tags,
    filter_prompts_by_tags,
)
import time


def _make_prompt(**kwargs):
    """Helper to create a Prompt with defaults."""
    defaults = {"title": "T", "content": "C"}
    defaults.update(kwargs)
    return Prompt(**defaults)


class TestSortPromptsByDate:
    """Tests for sort_prompts_by_date."""

    def test_descending_default(self):
        p1 = _make_prompt(title="Old")
        time.sleep(0.02)
        p2 = _make_prompt(title="New")
        result = sort_prompts_by_date([p1, p2])
        assert result[0].title == "New"

    def test_ascending(self):
        p1 = _make_prompt(title="Old")
        time.sleep(0.02)
        p2 = _make_prompt(title="New")
        result = sort_prompts_by_date([p1, p2], descending=False)
        assert result[0].title == "Old"

    def test_empty_list(self):
        assert sort_prompts_by_date([]) == []

    def test_single_item(self):
        p = _make_prompt()
        assert sort_prompts_by_date([p]) == [p]


class TestFilterByCollection:
    """Tests for filter_prompts_by_collection."""

    def test_filters_correctly(self):
        p1 = _make_prompt(collection_id="a")
        p2 = _make_prompt(collection_id="b")
        result = filter_prompts_by_collection([p1, p2], "a")
        assert len(result) == 1
        assert result[0].collection_id == "a"

    def test_no_match(self):
        p = _make_prompt(collection_id="a")
        assert filter_prompts_by_collection([p], "z") == []

    def test_empty_list(self):
        assert filter_prompts_by_collection([], "a") == []


class TestSearchPrompts:
    """Tests for search_prompts."""

    def test_search_by_title(self):
        p = _make_prompt(title="Python Tips")
        assert len(search_prompts([p], "python")) == 1

    def test_search_by_description(self):
        p = _make_prompt(description="Learn Java basics")
        assert len(search_prompts([p], "java")) == 1

    def test_case_insensitive(self):
        p = _make_prompt(title="UPPERCASE")
        assert len(search_prompts([p], "uppercase")) == 1

    def test_no_match(self):
        p = _make_prompt(title="Hello")
        assert search_prompts([p], "xyz") == []

    def test_none_description(self):
        p = _make_prompt(description=None)
        assert search_prompts([p], "anything") == []


class TestValidatePromptContent:
    """Tests for validate_prompt_content."""

    def test_valid(self):
        assert validate_prompt_content("This is valid content") is True

    def test_too_short(self):
        assert validate_prompt_content("Short") is False

    def test_empty(self):
        assert validate_prompt_content("") is False

    def test_whitespace_only(self):
        assert validate_prompt_content("   ") is False

    def test_exactly_10_chars(self):
        assert validate_prompt_content("1234567890") is True

    def test_9_chars(self):
        assert validate_prompt_content("123456789") is False


class TestExtractVariables:
    """Tests for extract_variables."""

    def test_single_variable(self):
        assert extract_variables("Hello {{name}}") == ["name"]

    def test_multiple_variables(self):
        result = extract_variables("{{a}} and {{b}}")
        assert result == ["a", "b"]

    def test_no_variables(self):
        assert extract_variables("No variables here") == []

    def test_nested_braces_ignored(self):
        assert extract_variables("{not_a_var}") == []

    def test_special_chars_not_captured(self):
        assert extract_variables("{{valid_1}}") == ["valid_1"]


class TestNormaliseTags:
    """Tests for normalise_tags."""

    def test_lowercase(self):
        assert normalise_tags(["Python", "AI"]) == ["python", "ai"]

    def test_strips_whitespace(self):
        assert normalise_tags(["  python  "]) == ["python"]

    def test_deduplicates(self):
        assert normalise_tags(["python", "Python", "PYTHON"]) == ["python"]

    def test_empty_list(self):
        assert normalise_tags([]) == []

    def test_preserves_order_of_first_occurrence(self):
        result = normalise_tags(["b", "a", "B"])
        assert result == ["b", "a"]


class TestFilterByTags:
    """Tests for filter_prompts_by_tags."""

    def test_single_tag_match(self):
        p1 = _make_prompt(tags=["python", "ai"])
        p2 = _make_prompt(tags=["java"])
        result = filter_prompts_by_tags([p1, p2], ["python"])
        assert len(result) == 1

    def test_multiple_tags_and_logic(self):
        p1 = _make_prompt(tags=["python", "ai"])
        p2 = _make_prompt(tags=["python"])
        result = filter_prompts_by_tags([p1, p2], ["python", "ai"])
        assert len(result) == 1

    def test_no_match(self):
        p = _make_prompt(tags=["java"])
        assert filter_prompts_by_tags([p], ["python"]) == []

    def test_empty_tags_filter(self):
        p = _make_prompt(tags=["python"])
        result = filter_prompts_by_tags([p], [])
        assert len(result) == 1

    def test_empty_prompts(self):
        assert filter_prompts_by_tags([], ["python"]) == []
