from pymongo import MongoClient
from fastapi import HTTPException
from bson import ObjectId
from bson.errors import InvalidId

client = MongoClient("mongodb://localhost:27017")
db = client["ecommerce"]
products_col = db["products"]


def _oid(product_id: str) -> ObjectId:
    try:
        return ObjectId(product_id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid product ID")


def serialize_product(product: dict):
    product["id"] = str(product["_id"])
    del product["_id"]
    return product


# -----------------------
# Create product
# -----------------------
def create_product(payload: dict):
    result = products_col.insert_one(payload)
    product = products_col.find_one({"_id": result.inserted_id})
    return serialize_product(product)


# -----------------------
# List products (optional filter)
# -----------------------
def list_products(min_stock: int | None = None):
    query = {}
    if min_stock is not None:
        query["quantity"] = {"$gte": min_stock}

    return [serialize_product(p) for p in products_col.find(query)]


# -----------------------
# Get product by ID
# -----------------------
def get_product(product_id: str):
    product = products_col.find_one({"_id": _oid(product_id)})
    if not product:
        raise HTTPException(404, "Product not found")
    return serialize_product(product)


# -----------------------
# Update inventory
# -----------------------
def update_inventory(product_id: str, quantity: int):
    result = products_col.update_one(
        {"_id": _oid(product_id)},
        {"$set": {"quantity": quantity}}
    )
    if result.matched_count == 0:
        raise HTTPException(404, "Product not found")

    return {"message": "Inventory updated", "quantity": quantity}


# -----------------------
# Purchase product (atomic)
# -----------------------
def purchase_product(product_id: str, quantity: int):
    product = products_col.find_one_and_update(
        {
            "_id": _oid(product_id),
            "quantity": {"$gte": quantity}
        },
        {"$inc": {"quantity": -quantity}},
        return_document=True
    )

    if not product:
        raise HTTPException(400, "Insufficient stock or product not found")

    return {
        "message": "Purchase successful",
        "remaining_quantity": product["quantity"]
    }
