from sqlalchemy.orm import Session

from app.models.note import Note
from app.models.user import User
from app.schemas.note import NoteCreate, NoteUpdate

from app.repositories.note_repository import (
    create_note,
    get_all_notes,
    get_note_by_id,
    get_notes_by_owner,
    update_note,
    delete_note,
    get_all_notes
)


def create_user_note(
    db: Session,
    note_data: NoteCreate,
    current_user: User,
    file_path: str | None = None
):
    note = Note(
        title=note_data.title,
        content=note_data.content,
        owner_id=current_user.id,
        file_path=file_path
    )

    return create_note(db, note)


def get_user_notes(
    db: Session,
    current_user: User
):
    return get_notes_by_owner(
        db,
        current_user.id
    )


def get_user_note(
    db: Session,
    note_id: int,
    current_user: User
):
    note = get_note_by_id(
        db,
        note_id
    )

    if not note:
        raise ValueError("Note not found")

    if note.owner_id != current_user.id:
        raise PermissionError(
            "You do not have permission to access this note"
        )

    return note


def update_user_note(
    db: Session,
    note_id: int,
    note_data: NoteUpdate,
    current_user: User
):
    note = get_note_by_id(
        db,
        note_id
    )

    if not note:
        raise ValueError("Note not found")

    if note.owner_id != current_user.id:
        raise PermissionError(
            "You do not have permission to update this note"
        )

    if note_data.title is not None:
        note.title = note_data.title

    if note_data.content is not None:
        note.content = note_data.content

    return update_note(db, note)


def delete_user_note(
    db: Session,
    note_id: int,
    current_user: User
):
    note = get_note_by_id(
        db,
        note_id
    )

    if not note:
        raise ValueError("Note not found")

    if note.owner_id != current_user.id:
        raise PermissionError(
            "You do not have permission to delete this note"
        )

    delete_note(db, note)

def get_all_notes_for_admin(
    db: Session
):
    return get_all_notes(db)