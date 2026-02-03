from fastapi import APIRouter
from pydantic import BaseModel, Field
from app.api.inventory_api import (
    create_product,
    list_products,
    get_product,
    update_inventory,
    purchase_product
)

router = APIRouter(prefix="/products", tags=["Products"])


# -----------------------
# Schemas
# -----------------------
class ProductCreate(BaseModel):
    name: str = Field(..., min_length=2)
    description: str | None = None
    price: float = Field(..., gt=0)
    quantity: int = Field(..., ge=0)


class QuantityPayload(BaseModel):
    quantity: int = Field(..., gt=0)


# -----------------------
# Routes
# -----------------------
@router.post("/", status_code=201)
def add_product(payload: ProductCreate):
    return create_product(payload.model_dump())


@router.get("/")
def get_all_products(min_stock: int | None = None):
    return list_products(min_stock)


@router.get("/{product_id}")
def get_single_product(product_id: str):
    return get_product(product_id)


@router.patch("/{product_id}/inventory")
def set_inventory(product_id: str, payload: QuantityPayload):
    return update_inventory(product_id, payload.quantity)


@router.post("/{product_id}/purchase")
def buy_product(product_id: str, payload: QuantityPayload):
    return purchase_product(product_id, payload.quantity)
