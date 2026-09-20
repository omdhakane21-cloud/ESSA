from fastapi import APIRouter, HTTPException
from app.config.settings import ADMIN_USERNAME, ADMIN_PASSWORD
from app.schemas.auth import LoginRequest, TokenResponse
from app.utils.security import create_access_token

router = APIRouter()

@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest):
    if data.username != ADMIN_USERNAME or data.password != ADMIN_PASSWORD:
        raise HTTPException(401, "Invalid username or password")
    return {"access_token": create_access_token(), "token_type": "bearer"}

@router.get("/me")
def me():
    return {"username": ADMIN_USERNAME, "role": "admin"}
