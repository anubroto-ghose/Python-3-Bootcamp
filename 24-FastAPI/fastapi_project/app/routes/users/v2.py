from fastapi import APIRouter

router = APIRouter(prefix="/users", tags=["users-v2"])

@router.get("/{user_id}")
def get_user(user_id: int):
    return {"id": user_id, "name": f"New User {user_id}", "email": "x@y.com"}
