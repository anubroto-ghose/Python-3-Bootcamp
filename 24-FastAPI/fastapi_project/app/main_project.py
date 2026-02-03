# app/main_project.py
from fastapi import FastAPI, HTTPException
from starlette.responses import Response



from app.db.models import UserAnswer
from app.api import api
from app.inventory_routes import router as inventory_router

app = FastAPI(title="JSON Quiz API")





# ---- Existing APIs (UNCHANGED) ----

@app.get("/")
def root():
    return {"message": "Fast API in Python"}

@app.get("/users", status_code=200, tags=["Quiz"], summary="Get all the users")
def read_user():
    return api.read_user()

@app.get("/question/{position}", status_code=200, responses={400: {"description": "Error"}},
         tags=["Quiz"], summary="Get question by position")
def read_questions(position: int, response: Response):
    question = api.read_questions(position)

    if not question:
        raise HTTPException(status_code=400, detail="Question not found for the given position")

    return question

@app.get("/alternatives/{question_id}", status_code=200, responses={400: {"description": "Error"}},
         tags=["Quiz"], summary="Get alternatives by question ID")
def read_alternatives(question_id: int):
    alternatives =  api.read_alternatives(question_id)
    if not alternatives:
        raise HTTPException(status_code=400, detail="Alternatives not found for the given question ID")
    return alternatives


'''
Sample input:
{
  "user_id": 1,
  "answers": [
    {
      "question_id": 1,
      "alternative_id": 1
    },
    {
      "question_id": 2,
      "alternative_id": 6
    },
    {
      "question_id": 3,
      "alternative_id": 8
    }
  ]
}
'''
@app.post("/answer", status_code=201, tags=["Quiz"], summary="Calculates which cars match a user’s quiz answers.")
def create_answer(payload: UserAnswer):
    payload = payload.dict()
    return api.create_answer(payload)


@app.get("/result/{user_id}", status_code=200, tags=["Quiz"],
         summary="Get result by user ID. It’s a lookup table that links a user to recommended cars based on results.json.")
def read_result(user_id: int):
    return api.read_result(user_id)
