from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_session
from services.auth_service import AuthService
from pydantic import BaseModel

router = APIRouter(prefix="/auth", tags=["auth"])

class RegisterRequest(BaseModel):
    username: str
    password: str
    email: str

class LoginRequest(BaseModel):
    email: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = 'bearer'

@router.post("/register")
async def register(data: RegisterRequest, session: AsyncSession = Depends(get_session)):
    service = AuthService(session)
    try:
        user = await service.register(data.email,data.username, data.password)
        return {"id": user.id, "email": user.email, "username": user.username}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
@router.post("/login", response_model=TokenResponse)
async def login(data:LoginRequest, session: AsyncSession = Depends(get_session)):
    service = AuthService(session)
    try:
        token = await service.login(data.email, data.password)
        return TokenResponse(access_token=token)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))