"""Шаблон Jinja2 с данными (задание 9 средней)."""

from flask import Flask, render_template


USERS = [
    {"id": 1, "name": "Иван Иванов", "age": 30, "role": "admin"},
    {"id": 2, "name": "Пётр Петров", "age": 25, "role": "user"},
    {"id": 3, "name": "Анна Смирнова", "age": 28, "role": "user"},
    {"id": 4, "name": "Мария Сидорова", "age": 35, "role": "moderator"},
]


def create_app() -> Flask:
    """Создаёт Flask-приложение."""
    app = Flask(__name__)

    @app.route("/")
    def index():
        return render_template(
            "users.html",
            title="Список пользователей",
            users=USERS,
        )

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5001)