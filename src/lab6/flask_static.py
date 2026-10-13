"""Статическая страница + CSS (задание 3 средней)."""

from flask import Flask, render_template


def create_app() -> Flask:
    """Создаёт Flask-приложение."""
    app = Flask(__name__)

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/about")
    def about():
        return render_template("about.html")

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5000)