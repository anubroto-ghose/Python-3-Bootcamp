# app/main_basics.py
from fastapi import FastAPI, HTTPException

app = FastAPI(title="FastAPI Basics – Learning Mode")

@app.get("/")
def root():
    return {"message": "Welcome to FastAPI basics"}

@app.get("/items/{item_id}")
def get_item(item_id: int):
    return {
        "item_id": item_id,
        "description": "This endpoint demonstrates path parameters"
    }

@app.get("/search")
def search_items(q: str | None = None, limit: int = 10):
    return {
        "query": q,
        "limit": limit
    }

@app.post("/items", status_code=201)
def create_item(payload: dict):
    if "name" not in payload:
        raise HTTPException(status_code=400, detail="name is required")
    return {
        "message": "Item created",
        "item": payload
    }

@app.delete("/items/{item_id}", status_code=204)
def delete_item(item_id: int):
    return None
