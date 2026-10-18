from fastapi import APIRouter
from app.api.v1.endpoints import predict
from app import auth

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_router.include_router(
    predict.router, prefix="/transactions", tags=["Inference"]
)