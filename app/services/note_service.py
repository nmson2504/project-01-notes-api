from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import NoteModel
from app.schemas import NoteCreate


def list_notes(db: Session) -> list[NoteModel]:
    return db.scalars(select(NoteModel)).all()


def get_note_or_404(note_id: int, db: Session) -> NoteModel:
    note = db.get(NoteModel, note_id)
    if note is None:
        raise HTTPException(status_code=404, detail=f"Note {note_id} not found")
    return note


def create_note(payload: NoteCreate, db: Session) -> NoteModel:
    note = NoteModel(title=payload.title, content=payload.content)
    db.add(note)
    db.commit()
    db.refresh(note)
    return note


def update_note(note_id: int, payload: NoteCreate, db: Session) -> NoteModel:
    note = get_note_or_404(note_id, db)
    note.title = payload.title
    note.content = payload.content
    db.commit()
    db.refresh(note)
    return note


def delete_note(note_id: int, db: Session) -> None:
    note = get_note_or_404(note_id, db)
    db.delete(note)
    db.commit()
