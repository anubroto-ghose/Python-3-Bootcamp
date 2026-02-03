# File: app/routers/users.py
from fastapi import APIRouter, HTTPException, Query
from fastapi.params import Path

router = APIRouter(prefix='/items', tags=['Items'])

@router.get('/')
def list_items():
    return [{'id': 1, 'name': 'iPhone 17'}]

@router.get('/search')
def search_items(q: str = Query(None, min_length=3, max_length=50),
                 page: int = Query(1, ge=1),
                 limit: int = Query(10, ge=1, le=100)):
    return {'q': q, 'page': page, 'limit': limit, 'results': []}

@router.get('/{item_id}', summary='Get item by ID')
def get_item(item_id: int = Path(..., gt=1, description='Numeric ID of the item to get items')):
    return {'item_id': item_id, 'name': f'Item {item_id}'}



@router.post("/", status_code=201, summary='Create a new item')
def create_item(payload: dict):
    if "name" not in payload:
        raise HTTPException(status_code=400, detail="name is required")
    return {
        "message": "Item created",
        "item": payload
    }

@router.delete("/{item_id}", status_code=204, tags=['Items'], summary='Delete an item by its ID')
def delete_item(item_id: int):
    return None
