from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from app.database import get_db
from app.services import note_service
from app.schemas import Note, NoteCreate

router = APIRouter()


@router.get("/notes", response_model=list[Note])
def list_notes(db: Session = Depends(get_db)):
    return note_service.list_notes(db)


@router.get("/notes/{note_id}", response_model=Note)
def read_note(note_id: int, db: Session = Depends(get_db)):
    return note_service.get_note_or_404(note_id, db)


@router.post("/notes", status_code=201, response_model=Note)
def create_note(payload: NoteCreate, db: Session = Depends(get_db)):
    return note_service.create_note(payload, db)


@router.put("/notes/{note_id}", response_model=Note)
def update_note(
    note_id: int,
    payload: NoteCreate,
    db: Session = Depends(get_db),
):
    return note_service.update_note(note_id, payload, db)


@router.delete("/notes/{note_id}", status_code=204)
def delete_note(note_id: int, db: Session = Depends(get_db)):
    note_service.delete_note(note_id, db)
    return Response(status_code=204)