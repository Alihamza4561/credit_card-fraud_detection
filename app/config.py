import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
  PROJECT_NAME: str = "Credit Card Fraud Detection API"
  VERSION: str = "1.0.0"
  API_V1_STR: str = "/api/v1"

  SECRET_KEY: str = os.getenv(
      "SECRET_KEY", "super-secret-jwt-token-key-change-in-production-123456"
  )
  ALGORITHM: str = "HS256"
  ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

  MODEL_PATH: str = os.getenv("MODEL_PATH", "artifacts/model_bundle.joblib")
  ADMIN_USERNAME: str = os.getenv("ADMIN_USERNAME", "admin")
  ADMIN_PASSWORD: str = os.getenv("ADMIN_PASSWORD", "secret123")

  model_config = SettingsConfigDict(case_sensitive=True)


settings = Settings()