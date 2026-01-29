# inventory_api.py
from pymongo import MongoClient
from fastapi import HTTPException
from bson import ObjectId

client = MongoClient("mongodb://localhost:27017")
db = client["ecommerce"]
products_col = db["products"]


def serialize_product(product):
    product["id"] = str(product["_id"])
    del product["_id"]
    return product


# -----------------------
# Create product (Admin)
# -----------------------
def create_product(payload: dict):
    payload["quantity"] = int(payload["quantity"])
    result = products_col.insert_one(payload)
    product = products_col.find_one({"_id": result.inserted_id})
    return serialize_product(product)


# -----------------------
# List all products
# -----------------------
def list_products():
    products = []
    for product in products_col.find():
        products.append(serialize_product(product))
    return products


# -----------------------
# Get product by ID
# -----------------------
def get_product(product_id: str):
    product = products_col.find_one({"_id": ObjectId(product_id)})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return serialize_product(product)


# -----------------------
# Update inventory (Admin)
# -----------------------
def update_inventory(product_id: str, quantity: int):
    result = products_col.update_one(
        {"_id": ObjectId(product_id)},
        {"$set": {"quantity": quantity}}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Inventory updated", "quantity": quantity}


# -----------------------
# Purchase product
# -----------------------
def purchase_product(product_id: str, quantity: int):
    product = products_col.find_one({"_id": ObjectId(product_id)})

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if product["quantity"] < quantity:
        raise HTTPException(status_code=400, detail="Insufficient stock")

    new_quantity = product["quantity"] - quantity

    products_col.update_one(
        {"_id": ObjectId(product_id)},
        {"$set": {"quantity": new_quantity}}
    )

    return {
        "message": "Purchase successful",
        "remaining_quantity": new_quantity
    }
