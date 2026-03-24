"""Storage layer tests for PromptLab."""

from app.models import Prompt, Collection
from app.storage import Storage


class TestPromptStorage:
    """Tests for prompt CRUD in Storage."""

    def test_create_and_get(self):
        s = Storage()
        p = Prompt(title="T", content="C")
        s.create_prompt(p)
        assert s.get_prompt(p.id) == p

    def test_get_nonexistent(self):
        s = Storage()
        assert s.get_prompt("nope") is None

    def test_get_all_empty(self):
        s = Storage()
        assert s.get_all_prompts() == []

    def test_get_all(self):
        s = Storage()
        s.create_prompt(Prompt(title="A", content="C"))
        s.create_prompt(Prompt(title="B", content="C"))
        assert len(s.get_all_prompts()) == 2

    def test_update_existing(self):
        s = Storage()
        p = Prompt(title="Old", content="C")
        s.create_prompt(p)
        updated = Prompt(id=p.id, title="New", content="C")
        result = s.update_prompt(p.id, updated)
        assert result.title == "New"
        assert s.get_prompt(p.id).title == "New"

    def test_update_nonexistent(self):
        s = Storage()
        p = Prompt(title="T", content="C")
        assert s.update_prompt("nope", p) is None

    def test_delete_existing(self):
        s = Storage()
        p = Prompt(title="T", content="C")
        s.create_prompt(p)
        assert s.delete_prompt(p.id) is True
        assert s.get_prompt(p.id) is None

    def test_delete_nonexistent(self):
        s = Storage()
        assert s.delete_prompt("nope") is False

    def test_get_prompts_by_collection(self):
        s = Storage()
        s.create_prompt(Prompt(title="A", content="C", collection_id="col-1"))
        s.create_prompt(Prompt(title="B", content="C", collection_id="col-2"))
        result = s.get_prompts_by_collection("col-1")
        assert len(result) == 1
        assert result[0].title == "A"

    def test_get_prompts_by_collection_empty(self):
        s = Storage()
        assert s.get_prompts_by_collection("col-1") == []


class TestCollectionStorage:
    """Tests for collection CRUD in Storage."""

    def test_create_and_get(self):
        s = Storage()
        c = Collection(name="Dev")
        s.create_collection(c)
        assert s.get_collection(c.id) == c

    def test_get_nonexistent(self):
        s = Storage()
        assert s.get_collection("nope") is None

    def test_get_all(self):
        s = Storage()
        s.create_collection(Collection(name="A"))
        s.create_collection(Collection(name="B"))
        assert len(s.get_all_collections()) == 2

    def test_delete_existing(self):
        s = Storage()
        c = Collection(name="Dev")
        s.create_collection(c)
        assert s.delete_collection(c.id) is True
        assert s.get_collection(c.id) is None

    def test_delete_nonexistent(self):
        s = Storage()
        assert s.delete_collection("nope") is False


class TestClear:
    """Tests for the clear utility method."""

    def test_clear_removes_all(self):
        s = Storage()
        s.create_prompt(Prompt(title="T", content="C"))
        s.create_collection(Collection(name="C"))
        s.clear()
        assert s.get_all_prompts() == []
        assert s.get_all_collections() == []
