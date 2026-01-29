from fastapi import APIRouter
from app.api.inventory_api import (
    create_product,
    list_products,
    get_product,
    update_inventory,
    purchase_product
)

router = APIRouter(prefix="/products", tags=["Products"])

@router.post("/", status_code=201)
def add_product(payload: dict):
    return create_product(payload)

@router.get("/")
def get_all_products():
    return list_products()

@router.get("/{product_id}")
def get_single_product(product_id: str):
    return get_product(product_id)

@router.patch("/{product_id}/inventory")
def set_inventory(product_id: str, payload: dict):
    return update_inventory(product_id, payload["quantity"])

@router.post("/{product_id}/purchase")
def buy_product(product_id: str, payload: dict):
    return purchase_product(product_id, payload["quantity"])
