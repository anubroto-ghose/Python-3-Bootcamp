"""
Pydantic Models Tutorial - FastAPI Schemas
======================================================

- Basic BaseModel usage
- Field validation & examples
- Request/Response model patterns
- Nested models & lists
- Modern Pydantic v2 `model_config = ConfigDict(...)`
- ORM conversion (`from_attributes=True`)
- Optional fields & defaults
- Common validation scenarios

Use these models with FastAPI endpoints for automatic validation + docs!

Author: [Miraj Godha]
"""

from pydantic import BaseModel, Field, ConfigDict, validator
from typing import Optional, List
from datetime import datetime
from uuid import UUID


# =============================================================================
# 1. BASIC MODELS (Item Example)
# =============================================================================

class ItemBase(BaseModel):
    """
    Base model for Item - shared fields between Create/Read.

    Why? DRY principle - avoid duplicating common fields.
    """
    model_config = ConfigDict(
        str_min_length=1,
        str_max_length=100
    )
    name: str = Field(..., example='T-shirt')  # ... = REQUIRED field
    description: Optional[str] = Field(None, example='100% cotton')


class ItemCreate(ItemBase):
    """
    Model for POST /items request body.

    FastAPI will validate incoming JSON against this shape automatically.
    """
    model_config = ItemBase.model_config | ConfigDict(gt=0)  # Inherit + price > 0
    price: float = Field(..., example=199.99)


class ItemRead(ItemBase):
    """
    Model for response (GET /items, POST response).

    Use `model_validate(db_obj)` to convert ORM objects → Pydantic.
    """
    model_config = ItemBase.model_config | ConfigDict(from_attributes=True)
    id: int
    price: float


# =============================================================================
# 2. NESTED MODELS & LISTS (Order Example)
# =============================================================================

class OrderItem(BaseModel):
    """Single item in an order."""
    item_id: int = Field(..., example=1, ge=1)
    quantity: int = Field(1, example=2, ge=1, le=100)  # Default=1, constraints


class OrderCreate(BaseModel):
    """POST /orders request - contains list of OrderItem."""
    user_id: int = Field(..., example=123, ge=1)
    items: List[OrderItem] = Field(..., min_items=1)  # At least 1 item


class OrderRead(OrderCreate):
    """GET /orders response."""
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime


# =============================================================================
# 3. OPTIONAL FIELDS & DEFAULTS (User Example)
# =============================================================================

class UserBase(BaseModel):
    """User fields with optional bio."""
    username: str = Field(..., min_length=3, example='john_doe')
    bio: Optional[str] = Field(None, max_length=500)
    is_active: bool = Field(True, description='Active user flag')


class UserCreate(UserBase):
    """POST /users request."""
    password: str = Field(..., min_length=8)


class UserRead(UserBase):
    """GET /users response - hide password."""
    model_config = ConfigDict(from_attributes=True)
    id: int


# =============================================================================
# 4. VALIDATORS (Advanced Constraints)
# =============================================================================

class Person(BaseModel):
    """Example with custom validator."""
    name: str
    age: int = Field(..., gt=0)

    @validator('age')
    def age_must_be_positive(cls, v):
        """Custom validation - runs after Field(gt=0)."""
        if v < 18:
            raise ValueError('Must be 18+ for this service')
        return v


class RangeModel(BaseModel):
    """Example with root_validator for cross-field validation."""
    start: Optional[int] = None
    end: Optional[int] = None

    @validator('start', 'end')
    def ensure_positive(cls, v):
        if v is not None and v < 0:
            raise ValueError('Must be positive')
        return v


# =============================================================================
# 5. SPECIAL TYPES (Datetime, UUID)
# =============================================================================

class Event(BaseModel):
    """Handles datetime/UUID string → object conversion."""
    id: int
    timestamp: datetime  # "2026-02-01T12:00:00Z" → datetime object
    uid: UUID  # "123e4567-e89b-12d3-a456-426614174000" → UUID


# =============================================================================
# 6. ALIAS EXAMPLE (Flexible JSON keys)
# =============================================================================

class Product(BaseModel):
    """Accepts 'productName' in JSON but uses 'product_name' internally."""
    product_name: str = Field(..., alias='productName', example='Shoes')


# =============================================================================
# 7. SETTINGS (Environment Config)
# =============================================================================

class Settings(BaseModel):
    """
    Load config from .env file.

    Usage: settings = Settings(_env_file='.env')
    """
    model_config = ConfigDict(env_file='.env')
    app_name: str = Field(default='MyApp')
    database_url: str


# =============================================================================
# USAGE EXAMPLES (For Teaching)
# =============================================================================

if __name__ == "__main__":
    # 1. Create → Validate
    item_create = ItemCreate(name="T-shirt", description="Cotton", price=199.99)
    print("Valid create:", item_create.model_dump())


    # 2. ORM → Pydantic (pretend DB object)
    class FakeORM:
        def __init__(self, id, name, price):
            self.id, self.name, self.price = id, name, price


    db_item = FakeORM(1, "T-shirt", 199.99)
    item_read = ItemRead.model_validate(db_item)
    print("ORM → Pydantic:", item_read.model_dump())

    # 3. Validation fails → 422 error (FastAPI handles this)
    try:
        ItemCreate(name="", price=-1)  # Invalid!
    except Exception as e:
        print("Validation error:", e)

    print("\n Ready for FastAPI endpoints!")
