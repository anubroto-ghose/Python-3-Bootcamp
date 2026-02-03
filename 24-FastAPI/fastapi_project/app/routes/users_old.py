# File: app/routers/users.py
from fastapi import APIRouter

router = APIRouter(prefix='/users', tags=['users'])

@router.get('/')
def list_users():
    return [{'id': 1, 'name': 'Alice'}]

@router.get('/v1/{user_id}', summary='Get a user by their ID')
def get_user_v1(user_id: int):
    return {'id': user_id, 'name': f'User {user_id}'}

@router.get('/v2/{user_id}', summary='Get user details with new version')
def get_user_v2(user_id: int):
    return {'id': user_id, 'name': f'New User {user_id}'}

@router.post('/', status_code=201, summary='Create a new user')
def create_user(payload: dict):
    return {
        "message": "User created",
        "user": payload
    }

@router.delete('/{user_id}', status_code=204, summary='Delete a user by their ID')
def delete_user(user_id: int):
    return None