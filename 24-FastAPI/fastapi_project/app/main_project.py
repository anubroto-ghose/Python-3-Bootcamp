# app/main_project.py
from fastapi import FastAPI, HTTPException
from starlette.responses import Response
from fastapi.middleware.cors import CORSMiddleware


from app.db.models import UserAnswer
from app.api import api
from app.inventory_routes import router as inventory_router

app = FastAPI(title="E-commerce + Quiz API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # allow all for learning
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---- Project Routers ----
app.include_router(inventory_router)

# ---- Existing APIs (UNCHANGED) ----

@app.get("/")
def root():
    return {"message": "Fast API in Python"}

@app.get("/user")
def read_user():
    return api.read_user()

@app.get("/question/{position}", status_code=200)
def read_questions(position: int, response: Response):
    question = api.read_questions(position)

    if not question:
        raise HTTPException(status_code=400, detail="Error")

    return question

@app.get("/alternatives/{question_id}")
def read_alternatives(question_id: int):
    return api.read_alternatives(question_id)

@app.post("/answer", status_code=201)
def create_answer(payload: UserAnswer):
    payload = payload.dict()
    return api.create_answer(payload)

@app.get("/result/{user_id}")
def read_result(user_id: int):
    return api.read_result(user_id)
