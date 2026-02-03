from fastapi import APIRouter

router = APIRouter(prefix="/users", tags=["users-v1"])

@router.get("/{user_id}")
def get_user(user_id: int):
    return {"id": user_id, "name": f"User {user_id}"}
