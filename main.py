from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from code_test import ask_openai

app = FastAPI()
security = HTTPBearer()  # Initializes bearer token security

# Dummy token for testing
DUMMY_TOKEN = "cencora1234567"

class QuestionRequest(BaseModel):
    question: str

class AnswerResponse(BaseModel):
    answer: str

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials.credentials != DUMMY_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid or missing token")

@app.post("/ask", response_model=AnswerResponse, dependencies=[Depends(verify_token)])
async def ask_question(request: QuestionRequest):
    try:
        response = ask_openai(request.question)
        return {"answer": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
