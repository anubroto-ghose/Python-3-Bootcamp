# app/main_basics.py
from fastapi import FastAPI, HTTPException, Query
from app.routes.items import router as items_router
# from app.routes.users import router as users_router
from app.routes.users.v1 import router as v1_router
from app.routes.users.v2 import router as v2_router

app = FastAPI(title="FastAPI Basics – Learning Mode",
description = 'API for learning FastAPI',
version = '1.0.1'
)

# app.include_router(users_router)
app.include_router(items_router)
app.include_router(v1_router, prefix="/v1")
app.include_router(v2_router, prefix="/v2")

@app.get("/")
def root():
    return {"message": "Welcome to FastAPI basics"}

@app.get('/health', tags=['Health'], summary='Health check test function')
def health():
    return {'status': 'ok'}
