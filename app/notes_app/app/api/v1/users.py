from fastapi import APIRouter

router = APIRouter()

@router.get("/users")
async def get_users():
    return [{"username": "user1"}, {"username": "user2"}]

@router.post("/users")
async def create_user(user: dict):
    return {"username": user["username"], "message": "User created successfully."}