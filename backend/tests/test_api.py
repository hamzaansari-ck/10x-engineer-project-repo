"""API tests for PromptLab

These tests verify the API endpoints work correctly.
"""

import time
import pytest
from fastapi.testclient import TestClient


class TestHealth:
    """Tests for health endpoint."""

    def test_health_check(self, client: TestClient):
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data


class TestPrompts:
    """Tests for prompt endpoints."""

    def test_create_prompt(self, client: TestClient, sample_prompt_data):
        response = client.post("/prompts", json=sample_prompt_data)
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == sample_prompt_data["title"]
        assert data["content"] == sample_prompt_data["content"]
        assert "id" in data
        assert "created_at" in data

    def test_list_prompts_empty(self, client: TestClient):
        response = client.get("/prompts")
        assert response.status_code == 200
        data = response.json()
        assert data["prompts"] == []
        assert data["total"] == 0

    def test_list_prompts_with_data(self, client: TestClient, sample_prompt_data):
        client.post("/prompts", json=sample_prompt_data)
        response = client.get("/prompts")
        assert response.status_code == 200
        data = response.json()
        assert len(data["prompts"]) == 1
        assert data["total"] == 1

    def test_get_prompt_success(self, client: TestClient, sample_prompt_data):
        create_response = client.post("/prompts", json=sample_prompt_data)
        prompt_id = create_response.json()["id"]
        response = client.get(f"/prompts/{prompt_id}")
        assert response.status_code == 200
        assert response.json()["id"] == prompt_id

    # Bug #1 fix: should return 404, not 500
    def test_get_prompt_not_found(self, client: TestClient):
        response = client.get("/prompts/nonexistent-id")
        assert response.status_code == 404

    def test_delete_prompt(self, client: TestClient, sample_prompt_data):
        create_response = client.post("/prompts", json=sample_prompt_data)
        prompt_id = create_response.json()["id"]
        response = client.delete(f"/prompts/{prompt_id}")
        assert response.status_code == 204
        # Verify it's gone
        assert client.get(f"/prompts/{prompt_id}").status_code == 404

    def test_delete_prompt_not_found(self, client: TestClient):
        response = client.delete("/prompts/nonexistent-id")
        assert response.status_code == 404

    # Bug #2 fix: updated_at should change on PUT
    def test_update_prompt(self, client: TestClient, sample_prompt_data):
        create_response = client.post("/prompts", json=sample_prompt_data)
        prompt_id = create_response.json()["id"]
        original_updated_at = create_response.json()["updated_at"]

        time.sleep(0.05)

        updated_data = {
            "title": "Updated Title",
            "content": "Updated content for the prompt",
            "description": "Updated description",
        }
        response = client.put(f"/prompts/{prompt_id}", json=updated_data)
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Title"
        assert data["updated_at"] != original_updated_at

    def test_update_prompt_not_found(self, client: TestClient):
        data = {"title": "X", "content": "Some content here"}
        response = client.put("/prompts/nonexistent-id", json=data)
        assert response.status_code == 404

    # Bug #3 fix: newest prompt should come first
    def test_sorting_order(self, client: TestClient):
        client.post("/prompts", json={"title": "First", "content": "First prompt content"})
        time.sleep(0.05)
        client.post("/prompts", json={"title": "Second", "content": "Second prompt content"})

        response = client.get("/prompts")
        prompts = response.json()["prompts"]
        assert prompts[0]["title"] == "Second"
        assert prompts[1]["title"] == "First"

    # PATCH endpoint tests
    def test_patch_prompt_partial_update(self, client: TestClient, sample_prompt_data):
        create_response = client.post("/prompts", json=sample_prompt_data)
        prompt_id = create_response.json()["id"]

        time.sleep(0.05)

        response = client.patch(f"/prompts/{prompt_id}", json={"title": "Patched Title"})
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Patched Title"
        # Other fields unchanged
        assert data["content"] == sample_prompt_data["content"]
        assert data["description"] == sample_prompt_data["description"]
        # updated_at should change
        assert data["updated_at"] != create_response.json()["updated_at"]

    def test_patch_prompt_not_found(self, client: TestClient):
        response = client.patch("/prompts/nonexistent-id", json={"title": "X"})
        assert response.status_code == 404

    def test_patch_prompt_invalid_collection(self, client: TestClient, sample_prompt_data):
        create_response = client.post("/prompts", json=sample_prompt_data)
        prompt_id = create_response.json()["id"]
        response = client.patch(f"/prompts/{prompt_id}", json={"collection_id": "bad-id"})
        assert response.status_code == 400

    # Search & filter
    def test_search_prompts(self, client: TestClient):
        client.post("/prompts", json={"title": "Python Tips", "content": "Use list comprehensions"})
        client.post("/prompts", json={"title": "Java Guide", "content": "Use streams"})

        response = client.get("/prompts?search=python")
        data = response.json()
        assert data["total"] == 1
        assert data["prompts"][0]["title"] == "Python Tips"

    def test_filter_by_collection(self, client: TestClient, sample_collection_data, sample_prompt_data):
        col = client.post("/collections", json=sample_collection_data).json()
        prompt_data = {**sample_prompt_data, "collection_id": col["id"]}
        client.post("/prompts", json=prompt_data)
        client.post("/prompts", json={"title": "Other", "content": "No collection"})

        response = client.get(f"/prompts?collection_id={col['id']}")
        assert response.json()["total"] == 1


class TestCollections:
    """Tests for collection endpoints."""

    def test_create_collection(self, client: TestClient, sample_collection_data):
        response = client.post("/collections", json=sample_collection_data)
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == sample_collection_data["name"]
        assert "id" in data

    def test_list_collections(self, client: TestClient, sample_collection_data):
        client.post("/collections", json=sample_collection_data)
        response = client.get("/collections")
        assert response.status_code == 200
        assert len(response.json()["collections"]) == 1

    def test_get_collection_not_found(self, client: TestClient):
        response = client.get("/collections/nonexistent-id")
        assert response.status_code == 404

    def test_get_collection_success(self, client: TestClient, sample_collection_data):
        col = client.post("/collections", json=sample_collection_data).json()
        response = client.get(f"/collections/{col['id']}")
        assert response.status_code == 200
        assert response.json()["name"] == sample_collection_data["name"]

    # Bug #4 fix: orphaned prompts should have collection_id set to None
    def test_delete_collection_with_prompts(self, client: TestClient, sample_collection_data, sample_prompt_data):
        col = client.post("/collections", json=sample_collection_data).json()
        prompt_data = {**sample_prompt_data, "collection_id": col["id"]}
        prompt = client.post("/prompts", json=prompt_data).json()

        # Delete collection
        response = client.delete(f"/collections/{col['id']}")
        assert response.status_code == 204

        # Prompt should still exist but with collection_id = None
        updated_prompt = client.get(f"/prompts/{prompt['id']}").json()
        assert updated_prompt["collection_id"] is None

    def test_delete_collection_not_found(self, client: TestClient):
        response = client.delete("/collections/nonexistent-id")
        assert response.status_code == 404
