# app/api/v1/endpoints/auth.py
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from app.config import settings
from app.model.schemas import Token,PredictionResponse, TransactionPayload
from app.api.deps import get_current_user
from app.services.fraud_service import fraud_service

router = APIRouter()


@router.post("/evaluate", response_model=PredictionResponse)
def evaluate(
    payload: TransactionPayload,
    current_user: str = Depends(
        get_current_user
    ),  # <-- This triggers Swagger to show the Authorize button
):
    return fraud_service.predict(payload.amount, payload.v_features)

@router.post("/token", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.usernaSme != settings.API_USER or form_data.password != settings.API_PASSWORD:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Incorrect username or password"
        )
    
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    token = jwt.encode({"sub": form_data.username, "exp": expire}, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}