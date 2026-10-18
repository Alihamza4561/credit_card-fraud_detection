from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, status
from app.config import settings
from app.auth import router as auth_router, verify_token
from app.services.fraud_service import fraud_service
from app.model.schemas import TransactionInput, EvaluationResponse, HealthResponse

@asynccontextmanager
async def lifespan(app: FastAPI):
    fraud_service.load(settings.MODEL_PATH)
    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    lifespan=lifespan
)

app.include_router(auth_router, prefix=settings.API_V1_STR)

@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    return {
        "status": "healthy",
        "version": settings.VERSION,
        "model_loaded": fraud_service.is_loaded
    }

@app.post(
    f"{settings.API_V1_STR}/transactions/evaluate", 
    response_model=EvaluationResponse, 
    tags=["Inference"]
)
async def evaluate_transaction(
    payload: TransactionInput, 
    username: str = Depends(verify_token)
):
    try:
        return fraud_service.predict(payload.amount, payload.v_features)
    except Exception as e:
        # Log the exact error to console for debugging
        print(f"\n[INFERENCE ERROR TRACE]: {e}\n")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Inference error: {str(e)}"
        )