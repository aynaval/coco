from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from split_code import get_azure_openai_token, ask_openai_with_token

app = FastAPI()

class AskRequest(BaseModel):
    token: str
    question: str

@app.get("/get-token")
def get_token():
    try:
        token = get_azure_openai_token()
        return {"token": token}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting token: {str(e)}")

@app.post("/ask")
def ask_question(request: AskRequest):
    try:
        response = ask_openai_with_token(request.token, request.question)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting response: {str(e)}")
