"""Тесты Flask-приложений."""

import pytest
from src.lab6.flask_static import create_app as create_static_app
from src.lab6.flask_jinja import create_app as create_jinja_app


@pytest.fixture
def static_client():
    app = create_static_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def jinja_client():
    app = create_jinja_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


class TestFlaskStatic:
    def test_index(self, static_client):
        response = static_client.get("/")
        assert response.status_code == 200
        assert "Добро пожаловать".encode("utf-8") in response.data

    def test_about(self, static_client):
        response = static_client.get("/about")
        assert response.status_code == 200
        assert "О проекте".encode("utf-8") in response.data

    def test_404(self, static_client):
        response = static_client.get("/nonexistent")
        assert response.status_code == 404

    def test_static_css(self, static_client):
        """CSS доступен по /static/style.css."""
        response = static_client.get("/static/style.css")
        assert response.status_code == 200
        assert b"font-family" in response.data


class TestFlaskJinja:
    def test_users_page(self, jinja_client):
        response = jinja_client.get("/")
        assert response.status_code == 200
        assert "Иван Иванов".encode("utf-8") in response.data

    def test_count(self, jinja_client):
        response = jinja_client.get("/")
        assert "Всего пользователей: 4".encode("utf-8") in response.data

    def test_static_css(self, jinja_client):
        response = jinja_client.get("/static/style.css")
        assert response.status_code == 200
