"""Тесты FastAPI-приложений."""

import pytest
from fastapi.testclient import TestClient

from src.lab6.fastapi_json import app as json_app
from src.lab6 import fastapi_notes
from src.lab6.fastapi_notes import app as notes_app


@pytest.fixture
def json_client():
    return TestClient(json_app)


@pytest.fixture
def notes_client():
    fastapi_notes._notes.clear()
    fastapi_notes._next_id = 1
    return TestClient(notes_app)


class TestFastAPIJson:
    def test_root(self, json_client):
        response = json_client.get("/")
        assert response.status_code == 200
        assert response.json()["message"] == "Привет от FastAPI!"

    def test_info(self, json_client):
        response = json_client.get("/api/info")
        assert response.status_code == 200
        assert response.json()["variant"] == 7

    def test_health(self, json_client):
        response = json_client.get("/api/health")
        assert response.status_code == 200


class TestFastAPINotes:
    def test_empty(self, notes_client):
        response = notes_client.get("/notes")
        assert response.status_code == 200
        assert response.json() == []

    def test_create(self, notes_client):
        response = notes_client.post(
            "/notes", json={"title": "Тест", "content": "Текст"}
        )
        assert response.status_code == 201
        assert response.json()["title"] == "Тест"

    def test_get(self, notes_client):
        notes_client.post("/notes", json={"title": "A", "content": "B"})
        response = notes_client.get("/notes/1")
        assert response.status_code == 200

    def test_get_missing(self, notes_client):
        response = notes_client.get("/notes/999")
        assert response.status_code == 404

    def test_update(self, notes_client):
        notes_client.post("/notes", json={"title": "Old", "content": ""})
        response = notes_client.put(
            "/notes/1", json={"title": "New", "content": "X"}
        )
        assert response.status_code == 200
        assert response.json()["title"] == "New"

    def test_delete(self, notes_client):
        notes_client.post("/notes", json={"title": "Del", "content": ""})
        response = notes_client.delete("/notes/1")
        assert response.status_code == 204

    def test_validation_empty_title(self, notes_client):
        response = notes_client.post("/notes", json={"title": "", "content": ""})
        assert response.status_code == 422