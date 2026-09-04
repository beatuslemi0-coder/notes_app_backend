from fastapi import APIRouter, Depends

from app.api.dependencies import get_current_user,require_role
from app.db import session
from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserResponse
from app.services.user_service import get_all_users_for_admin


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get(
    "/me",
    response_model=UserResponse
)
def get_me(
    current_user: User = Depends(get_current_user)
):
    return current_user
@router.get(
    "/admin-test"
)
def admin_test(
    current_user: User = Depends(
        require_role("admin")
    )
):
    return {
        "message": "Welcome Admin",
        "user_id": current_user.id,
        "role": current_user.role
    }

@router.get(
    "/admin/users",
    response_model=list[UserResponse]
)
def get_all_users(
    current_user: User = Depends(
        require_role("admin")
    ),
    db: session = Depends(get_db)
):
    return get_all_users_for_admin(db)