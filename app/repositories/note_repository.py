from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.note import Note


def create_note(
    db: Session,
    note: Note
):
    db.add(note)
    db.commit()
    db.refresh(note)

    return note


def get_note_by_id(
    db: Session,
    note_id: int
):
    statement = select(Note).where(
        Note.id == note_id
    )

    return db.scalar(statement)


def get_notes_by_owner(
    db: Session,
    owner_id: int
):
    statement = select(Note).where(
        Note.owner_id == owner_id
    )

    return list(db.scalars(statement).all())


def update_note(
    db: Session,
    note: Note
):
    db.commit()
    db.refresh(note)

    return note


def delete_note(
    db: Session,
    note: Note
):
    db.delete(note)
    db.commit()

def get_all_notes(
    db: Session
):
    statement = select(Note)

    return list(db.scalars(statement).all())  