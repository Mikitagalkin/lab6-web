"""FastAPI JSON endpoint (задание 7 средней)."""

from fastapi import FastAPI
from pydantic import BaseModel


class InfoResponse(BaseModel):
    """Ответ /api/info."""
    name: str
    version: str
    author: str
    lab: int
    variant: int


app = FastAPI(
    title="ЛР6 FastAPI JSON",
    description="Задание 7 средней сложности, вариант 7",
    version="1.0.0",
)


@app.get("/")
def root():
    return {"message": "Привет от FastAPI!"}


@app.get("/api/info", response_model=InfoResponse)
def get_info():
    """Возвращает информацию о проекте в JSON."""
    return InfoResponse(
        name="lab6-web",
        version="1.0.0",
        author="Сидяк Никита Андреевич",
        lab=6,
        variant=7,
    )


@app.get("/api/health")
def health():
    """Проверка работоспособности."""
    return {"status": "ok"}