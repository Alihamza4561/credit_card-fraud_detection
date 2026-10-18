from typing import List
from pydantic import BaseModel, Field


class TransactionInput(BaseModel):
  amount: float = Field(
      ...,
      gt=0,
      description="Transaction amount in USD",
      json_schema_extra={"example": 149.99},
  )
  v_features: List[float] = Field(
      ...,
      min_length=28,
      max_length=28,
      description="28 PCA transformed features (V1-V28)",
  )
class EvaluationResponse(BaseModel):
    is_fraud: bool
    fraud_probability: float
    decision_threshold: float
    status: str

class Token(BaseModel):
    access_token: str
    token_type: str

class HealthResponse(BaseModel):
    status: str
    version: str
    model_loaded: bool