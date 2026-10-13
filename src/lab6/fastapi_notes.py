"""REST API для заметок (задание 5 повышенной)."""

from datetime import datetime

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field


class NoteBase(BaseModel):
    """Базовые поля заметки."""
    title: str = Field(..., min_length=1, max_length=100)
    content: str = Field("", max_length=1000)


class NoteCreate(NoteBase):
    """Схема создания."""
    pass


class NoteUpdate(NoteBase):
    """Схема обновления."""
    pass


class Note(NoteBase):
    """Схема заметки с ID и датой."""
    id: int
    created_at: datetime


_notes: dict = {}
_next_id = 1


def _generate_id() -> int:
    """Автоинкремент ID."""
    global _next_id
    new_id = _next_id
    _next_id += 1
    return new_id


app = FastAPI(
    title="ЛР6 REST API заметок",
    description="Задание 5 повышенной сложности, вариант 7",
    version="1.0.0",
)


@app.get("/", tags=["root"])
def root():
    return {"message": "Notes API", "docs": "/docs"}


@app.get("/notes", response_model=list[Note], tags=["notes"])
def list_notes():
    """Возвращает все заметки."""
    return list(_notes.values())


@app.get("/notes/{note_id}", response_model=Note, tags=["notes"])
def get_note(note_id: int):
    """Возвращает заметку по ID."""
    if note_id not in _notes:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Заметка {note_id} не найдена",
        )
    return _notes[note_id]


@app.post(
    "/notes",
    response_model=Note,
    status_code=status.HTTP_201_CREATED,
    tags=["notes"],
)
def create_note(payload: NoteCreate):
    """Создаёт новую заметку."""
    note_id = _generate_id()
    note = Note(
        id=note_id,
        title=payload.title,
        content=payload.content,
        created_at=datetime.now(),
    )
    _notes[note_id] = note
    return note


@app.put("/notes/{note_id}", response_model=Note, tags=["notes"])
def update_note(note_id: int, payload: NoteUpdate):
    """Обновляет заметку."""
    if note_id not in _notes:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Заметка {note_id} не найдена",
        )
    old = _notes[note_id]
    updated = Note(
        id=note_id,
        title=payload.title,
        content=payload.content,
        created_at=old.created_at,
    )
    _notes[note_id] = updated
    return updated


@app.delete(
    "/notes/{note_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["notes"],
)
def delete_note(note_id: int):
    """Удаляет заметку."""
    if note_id not in _notes:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Заметка {note_id} не найдена",
        )
    del _notes[note_id]
    return None