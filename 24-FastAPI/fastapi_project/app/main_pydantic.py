"""
Complete FastAPI CRUD Demo with Pydantic Validation
===============================================

✅ POST - Create data
✅ GET  - Fetch data (list + single)
✅ PUT  - Update data
✅ DELETE - Remove data
✅ In-memory data storage (dict)
✅ Full CRUD workflow with Pydantic validation

Run: uvicorn app.main_pydantic:app --reload
Swagger: http://127.0.0.1:8000/docs
"""

from fastapi import FastAPI, HTTPException, Path
from typing import List
import uvicorn

from app.schemas.items import ItemCreate, ItemRead, ItemBase  # Your Pydantic models

# In-memory DB (dict) - replace with SQLAlchemy later
DB: dict[int, dict] = {}
NEXT_ID: int = 1

app = FastAPI(title="Full CRUD Pydantic Demo", version="1.0")

# =============================================================================
# ✅ POST - CREATE DATA
# =============================================================================
@app.post("/items", response_model=ItemRead, status_code=201)
def create_item(item: ItemCreate):
    """Create new item - validates ItemCreate automatically."""
    global NEXT_ID
    record = item.model_dump()
    # print("record: " , record)
    record["id"] = NEXT_ID
    DB[NEXT_ID] = record
    # print("Next id: " , NEXT_ID)
    # print("DB: " , DB)
    NEXT_ID += 1
    return record

# =============================================================================
# ✅ GET - FETCH DATA (List + Single)
# =============================================================================
@app.get("/items", response_model=List[ItemRead])
def list_items():
    """Fetch all items."""
    return list(DB.values())


@app.head("/items")
def head_items():
    """
    HEAD /items - Check if items exist (headers only).

    Returns: 200 OK if items exist, 404 if empty.
    """
    if not DB:
        raise HTTPException(status_code=404, detail="No items")
    return {}  # Empty body = HEAD behavior

@app.get("/items/{item_id}", response_model=ItemRead)
def get_item(item_id: int = Path(..., ge=1, description="Item ID")):
    """Fetch single item by ID."""
    item = DB.get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@app.head("/items/{item_id}")
def head_item(item_id: int = Path(..., ge=1)):
    """
    HEAD /items/{id} - Check if specific item exists.

    Returns: 200 OK if exists, 404 if not.
    """
    if item_id not in DB:
        raise HTTPException(status_code=404, detail="Item not found")
    return {}  # Empty body

# =============================================================================
# ✅ PUT - UPDATE DATA (Full Replace)
# =============================================================================
@app.put("/items/{item_id}", response_model=ItemRead)
def update_item(item_id: int = Path(..., ge=1),
                item: ItemCreate = None):
    """
    Update existing item (full replace).

    If item missing → Creates new (upsert behavior).
    """
    if item_id not in DB:
        raise HTTPException(status_code=404, detail="Item not found")

    record = item.model_dump()
    record["id"] = item_id  # Preserve ID
    DB[item_id] = record
    return record

# =============================================================================
# ✅ DELETE - REMOVE DATA
# =============================================================================
@app.delete("/items/{item_id}", status_code=204)
def delete_item(item_id: int = Path(..., ge=1)):
    """Delete item by ID. Returns 204 No Content."""
    if item_id not in DB:
        raise HTTPException(status_code=404, detail="Item not found")
    del DB[item_id]

# =============================================================================
# 🛡️ ERROR HANDLING & UTILS
# =============================================================================
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    """Custom 422: 'Validation failed' + details."""
    return JSONResponse(
        status_code=422,
        content={"error": "Sippai shimashitha", "details": exc.errors()}
    )

@app.get("/health")
def health_check():
    """Health check + DB stats."""
    return {
        "status": "healthy",
        "total_items": len(DB),
        "next_id": NEXT_ID - 1
    }

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
