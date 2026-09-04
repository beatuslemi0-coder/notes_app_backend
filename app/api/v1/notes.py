from fastapi import APIRouter, Depends, HTTPException, status,UploadFile,File,Form
from sqlalchemy.orm import Session
from app.services.file_service import save_uploaded_file

from app.api.dependencies import get_current_user,require_role
from app.db.session import get_db
from app.models.user import User
from app.schemas.note import (
    NoteCreate,
    NoteUpdate,
    NoteResponse
)
from app.services.note_service import (
    create_user_note,
    get_user_notes,
    get_user_note,
    update_user_note,
    delete_user_note,
    get_all_notes_for_admin
)


router = APIRouter(
    prefix="/notes",
    tags=["Notes"]
)

@router.post(
    "",
    response_model=NoteResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_note(
    title: str = Form(...),
    content: str = Form(...),
    file: UploadFile | None = File(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        file_path = None

        if file:
            file_path = await save_uploaded_file(file)

        note_data = NoteCreate(
            title=title,
            content=content
        )

        return create_user_note(
            db,
            note_data,
            current_user,
            file_path
        )

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )


@router.get(
    "",
    response_model=list[NoteResponse]
)
def get_notes(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_user_notes(
        db,
        current_user
    )

@router.get(
    "/{note_id}",
    response_model=NoteResponse
)
def get_note(
    note_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        return get_user_note(
            db,
            note_id,
            current_user
        )

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error)
        )

    except PermissionError as error:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(error)
        )

@router.put(
    "/{note_id}",
    response_model=NoteResponse
)
def update_note(
    note_id: int,
    note_data: NoteUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        return update_user_note(
            db,
            note_id,
            note_data,
            current_user
        )

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error)
        )

    except PermissionError as error:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(error)
        )

@router.delete(
    "/{note_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_note(
    note_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        delete_user_note(
            db,
            note_id,
            current_user
        )

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error)
        )

    except PermissionError as error:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(error)
        )

@router.get(
    "/admin/all",
    response_model=list[NoteResponse]
)
def get_all_notes_admin(
    current_user: User = Depends(
        require_role("admin")
    ),
    db: Session = Depends(get_db)
):
    return get_all_notes_for_admin(db)

