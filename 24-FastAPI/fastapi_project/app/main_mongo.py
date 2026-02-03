from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.inventory_routes import router as inventory_router

app = FastAPI(title="Mongo DB E-commerce")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # allow all for learning
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---- Project Routers ----
app.include_router(inventory_router)

@app.get("/")
def root():
    return {"message": "Mongo DB E-commerce API"}