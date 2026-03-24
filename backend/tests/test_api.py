"""API tests for PromptLab.

Comprehensive test suite covering all endpoints, error cases, edge cases,
and the tagging feature.
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


class TestCreatePrompt:
    """Tests for POST /prompts."""

    def test_create_minimal(self, client: TestClient):
        response = client.post("/prompts", json={"title": "T", "content": "C"})
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "T"
        assert data["tags"] == []
        assert "id" in data
        assert "created_at" in data
        assert "updated_at" in data

    def test_create_full(self, client: TestClient, sample_prompt_data):
        response = client.post("/prompts", json=sample_prompt_data)
        assert response.status_code == 201
        assert response.json()["description"] == sample_prompt_data["description"]

    def test_create_with_collection(self, client: TestClient, sample_collection_data):
        col = client.post("/collections", json=sample_collection_data).json()
        data = {"title": "T", "content": "C", "collection_id": col["id"]}
        response = client.post("/prompts", json=data)
        assert response.status_code == 201
        assert response.json()["collection_id"] == col["id"]

    def test_create_invalid_collection(self, client: TestClient):
        data = {"title": "T", "content": "C", "collection_id": "bad"}
        assert client.post("/prompts", json=data).status_code == 400

    def test_create_empty_title(self, client: TestClient):
        assert client.post("/prompts", json={"title": "", "content": "C"}).status_code == 422

    def test_create_empty_content(self, client: TestClient):
        assert client.post("/prompts", json={"title": "T", "content": ""}).status_code == 422

    def test_create_with_tags(self, client: TestClient):
        data = {"title": "T", "content": "C", "tags": ["Python", " AI "]}
        response = client.post("/prompts", json=data)
        assert response.status_code == 201
        assert response.json()["tags"] == ["python", "ai"]

    def test_create_tags_deduplicated(self, client: TestClient):
        data = {"title": "T", "content": "C", "tags": ["python", "Python"]}
        response = client.post("/prompts", json=data)
        assert response.json()["tags"] == ["python"]


class TestListPrompts:
    """Tests for GET /prompts."""

    def test_empty(self, client: TestClient):
        response = client.get("/prompts")
        assert response.status_code == 200
        assert response.json() == {"prompts": [], "total": 0}

    def test_with_data(self, client: TestClient, sample_prompt_data):
        client.post("/prompts", json=sample_prompt_data)
        data = client.get("/prompts").json()
        assert data["total"] == 1

    def test_sorting_newest_first(self, client: TestClient):
        client.post("/prompts", json={"title": "First", "content": "C"})
        time.sleep(0.05)
        client.post("/prompts", json={"title": "Second", "content": "C"})
        prompts = client.get("/prompts").json()["prompts"]
        assert prompts[0]["title"] == "Second"

    def test_search(self, client: TestClient):
        client.post("/prompts", json={"title": "Python Tips", "content": "C"})
        client.post("/prompts", json={"title": "Java Guide", "content": "C"})
        data = client.get("/prompts?search=python").json()
        assert data["total"] == 1
        assert data["prompts"][0]["title"] == "Python Tips"

    def test_search_no_match(self, client: TestClient):
        client.post("/prompts", json={"title": "Hello", "content": "C"})
        assert client.get("/prompts?search=xyz").json()["total"] == 0

    def test_filter_by_collection(self, client: TestClient, sample_collection_data):
        col = client.post("/collections", json=sample_collection_data).json()
        client.post("/prompts", json={"title": "In", "content": "C", "collection_id": col["id"]})
        client.post("/prompts", json={"title": "Out", "content": "C"})
        assert client.get(f"/prompts?collection_id={col['id']}").json()["total"] == 1

    def test_filter_by_tag(self, client: TestClient):
        client.post("/prompts", json={"title": "A", "content": "C", "tags": ["python", "ai"]})
        client.post("/prompts", json={"title": "B", "content": "C", "tags": ["java"]})
        data = client.get("/prompts?tag=python").json()
        assert data["total"] == 1
        assert data["prompts"][0]["title"] == "A"

    def test_filter_by_multiple_tags(self, client: TestClient):
        client.post("/prompts", json={"title": "A", "content": "C", "tags": ["python", "ai"]})
        client.post("/prompts", json={"title": "B", "content": "C", "tags": ["python"]})
        data = client.get("/prompts?tag=python&tag=ai").json()
        assert data["total"] == 1
        assert data["prompts"][0]["title"] == "A"


class TestGetPrompt:
    """Tests for GET /prompts/{id}."""

    def test_success(self, client: TestClient, sample_prompt_data):
        prompt = client.post("/prompts", json=sample_prompt_data).json()
        response = client.get(f"/prompts/{prompt['id']}")
        assert response.status_code == 200
        assert response.json()["id"] == prompt["id"]

    def test_not_found(self, client: TestClient):
        assert client.get("/prompts/nonexistent").status_code == 404


class TestUpdatePrompt:
    """Tests for PUT /prompts/{id}."""

    def test_success(self, client: TestClient, sample_prompt_data):
        prompt = client.post("/prompts", json=sample_prompt_data).json()
        time.sleep(0.05)
        updated = {"title": "New", "content": "New content"}
        response = client.put(f"/prompts/{prompt['id']}", json=updated)
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "New"
        assert data["updated_at"] != prompt["updated_at"]

    def test_not_found(self, client: TestClient):
        data = {"title": "T", "content": "C"}
        assert client.put("/prompts/nope", json=data).status_code == 404

    def test_invalid_collection(self, client: TestClient, sample_prompt_data):
        prompt = client.post("/prompts", json=sample_prompt_data).json()
        data = {"title": "T", "content": "C", "collection_id": "bad"}
        assert client.put(f"/prompts/{prompt['id']}", json=data).status_code == 400

    def test_update_with_tags(self, client: TestClient, sample_prompt_data):
        prompt = client.post("/prompts", json=sample_prompt_data).json()
        data = {"title": "T", "content": "C", "tags": ["New", "TAGS"]}
        response = client.put(f"/prompts/{prompt['id']}", json=data)
        assert response.json()["tags"] == ["new", "tags"]


class TestPatchPrompt:
    """Tests for PATCH /prompts/{id}."""

    def test_partial_title(self, client: TestClient, sample_prompt_data):
        prompt = client.post("/prompts", json=sample_prompt_data).json()
        time.sleep(0.05)
        response = client.patch(f"/prompts/{prompt['id']}", json={"title": "Patched"})
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Patched"
        assert data["content"] == sample_prompt_data["content"]
        assert data["updated_at"] != prompt["updated_at"]

    def test_not_found(self, client: TestClient):
        assert client.patch("/prompts/nope", json={"title": "X"}).status_code == 404

    def test_invalid_collection(self, client: TestClient, sample_prompt_data):
        prompt = client.post("/prompts", json=sample_prompt_data).json()
        assert client.patch(
            f"/prompts/{prompt['id']}", json={"collection_id": "bad"}
        ).status_code == 400

    def test_patch_tags(self, client: TestClient, sample_prompt_data):
        prompt = client.post("/prompts", json=sample_prompt_data).json()
        response = client.patch(f"/prompts/{prompt['id']}", json={"tags": ["New"]})
        assert response.json()["tags"] == ["new"]

    def test_patch_empty_body(self, client: TestClient, sample_prompt_data):
        prompt = client.post("/prompts", json=sample_prompt_data).json()
        response = client.patch(f"/prompts/{prompt['id']}", json={})
        assert response.status_code == 200


class TestDeletePrompt:
    """Tests for DELETE /prompts/{id}."""

    def test_success(self, client: TestClient, sample_prompt_data):
        prompt = client.post("/prompts", json=sample_prompt_data).json()
        assert client.delete(f"/prompts/{prompt['id']}").status_code == 204
        assert client.get(f"/prompts/{prompt['id']}").status_code == 404

    def test_not_found(self, client: TestClient):
        assert client.delete("/prompts/nope").status_code == 404


class TestCollections:
    """Tests for collection endpoints."""

    def test_create(self, client: TestClient, sample_collection_data):
        response = client.post("/collections", json=sample_collection_data)
        assert response.status_code == 201
        assert response.json()["name"] == sample_collection_data["name"]
        assert "id" in response.json()

    def test_create_empty_name(self, client: TestClient):
        assert client.post("/collections", json={"name": ""}).status_code == 422

    def test_list(self, client: TestClient, sample_collection_data):
        client.post("/collections", json=sample_collection_data)
        data = client.get("/collections").json()
        assert len(data["collections"]) == 1
        assert data["total"] == 1

    def test_list_empty(self, client: TestClient):
        data = client.get("/collections").json()
        assert data["total"] == 0

    def test_get_success(self, client: TestClient, sample_collection_data):
        col = client.post("/collections", json=sample_collection_data).json()
        response = client.get(f"/collections/{col['id']}")
        assert response.status_code == 200
        assert response.json()["name"] == sample_collection_data["name"]

    def test_get_not_found(self, client: TestClient):
        assert client.get("/collections/nope").status_code == 404

    def test_delete_success(self, client: TestClient, sample_collection_data):
        col = client.post("/collections", json=sample_collection_data).json()
        assert client.delete(f"/collections/{col['id']}").status_code == 204
        assert client.get(f"/collections/{col['id']}").status_code == 404

    def test_delete_not_found(self, client: TestClient):
        assert client.delete("/collections/nope").status_code == 404

    def test_delete_nullifies_prompts(self, client: TestClient, sample_collection_data, sample_prompt_data):
        col = client.post("/collections", json=sample_collection_data).json()
        prompt = client.post(
            "/prompts", json={**sample_prompt_data, "collection_id": col["id"]}
        ).json()
        client.delete(f"/collections/{col['id']}")
        updated = client.get(f"/prompts/{prompt['id']}").json()
        assert updated["collection_id"] is None

    def test_delete_multiple_prompts_nullified(self, client: TestClient, sample_collection_data):
        col = client.post("/collections", json=sample_collection_data).json()
        p1 = client.post("/prompts", json={"title": "A", "content": "C", "collection_id": col["id"]}).json()
        p2 = client.post("/prompts", json={"title": "B", "content": "C", "collection_id": col["id"]}).json()
        client.delete(f"/collections/{col['id']}")
        assert client.get(f"/prompts/{p1['id']}").json()["collection_id"] is None
        assert client.get(f"/prompts/{p2['id']}").json()["collection_id"] is None


class TestTags:
    """Tests for GET /tags endpoint."""

    def test_empty(self, client: TestClient):
        data = client.get("/tags").json()
        assert data["tags"] == []

    def test_counts(self, client: TestClient):
        client.post("/prompts", json={"title": "A", "content": "C", "tags": ["python", "ai"]})
        client.post("/prompts", json={"title": "B", "content": "C", "tags": ["python"]})
        data = client.get("/tags").json()
        tags_dict = {t["name"]: t["count"] for t in data["tags"]}
        assert tags_dict["python"] == 2
        assert tags_dict["ai"] == 1

    def test_sorted_by_count(self, client: TestClient):
        client.post("/prompts", json={"title": "A", "content": "C", "tags": ["rare"]})
        client.post("/prompts", json={"title": "B", "content": "C", "tags": ["common"]})
        client.post("/prompts", json={"title": "C", "content": "C", "tags": ["common"]})
        data = client.get("/tags").json()
        assert data["tags"][0]["name"] == "common"
        assert data["tags"][0]["count"] == 2
