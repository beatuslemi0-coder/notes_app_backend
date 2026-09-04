from sqlalchemy.orm import Session

from app import db
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import hash_password
from app.repositories.user_repository import (
    get_user_by_email,
    get_user_by_username,
    create_user,
    get_all_users
)


def register_user(
    db: Session,
    user_data: UserCreate
):
    existing_email = get_user_by_email(
        db,
        user_data.email
    )

    if existing_email:
        raise ValueError("Email already registered")

    existing_username = get_user_by_username(
        db,
        user_data.username
    )

    if existing_username:
        raise ValueError("Username already taken")

    hashed_password = hash_password(
        user_data.password
    )

    user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_password,
        role="user",
        is_active=True
    )

    return create_user(db, user)
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token
)

from app.schemas.user import (
    UserCreate,
    LoginRequest
)

from app.repositories.user_repository import (
    get_user_by_email,
    get_user_by_username,
    create_user
)
def login_user(
    db: Session,
    username: str,
    password: str
):
    user = get_user_by_email(
        db,
        username
    )

    if not user:
        raise ValueError("Invalid email or password")

    if not verify_password(
        password,
        user.hashed_password
    ):
        raise ValueError("Invalid email or password")

    if not user.is_active:
        raise ValueError("User account is inactive")

    access_token = create_access_token({
        "sub": str(user.id),
        "role": user.role
    })

    return access_token

def get_all_users_for_admin(
    db: Session
):
    return get_all_users(db)