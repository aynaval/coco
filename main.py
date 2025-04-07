from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from split_code import get_azure_openai_token, ask_openai_with_token

app = FastAPI()

# Dummy token
DUMMY_BEARER_TOKEN = "cencora123"

# FastAPI security scheme
security = HTTPBearer()

# Dependency that checks the token
def verify_bearer_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials.scheme.lower() != "bearer" or credentials.credentials != DUMMY_BEARER_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid or missing bearer token")

class AskRequest(BaseModel):
    token: str
    question: str

@app.get("/get-token", dependencies=[Depends(verify_bearer_token)])
def get_token():
    try:
        token = get_azure_openai_token()
        return {"token": token}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting token: {str(e)}")

@app.post("/ask", dependencies=[Depends(verify_bearer_token)])
def ask_question(request: AskRequest):
    try:
        response = ask_openai_with_token(request.token, request.question)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting response: {str(e)}")
