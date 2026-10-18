import logging
import joblib
import pandas as pd

logger = logging.getLogger("uvicorn")


class FraudService:

  def __init__(self):
    self.pipeline = None
    self.feature_names = None
    self.threshold = 0.5
    self.is_loaded = False

  def load(self, model_path: str):
    try:
      bundle = joblib.load(model_path)
      if isinstance(bundle, dict):
        self.pipeline = bundle.get("pipeline")
        self.feature_names = bundle.get("feature_names")
        self.threshold = bundle.get("threshold", 0.5)
      else:
        self.pipeline = bundle
        self.threshold = 0.5

      # Extract feature names directly from the fitted scaler/estimator if missing from bundle
      if not self.feature_names:
        if hasattr(self.pipeline, "feature_names_in_"):
          self.feature_names = list(self.pipeline.feature_names_in_)
        elif hasattr(self.pipeline, "steps") and hasattr(
            self.pipeline.steps[0][1], "feature_names_in_"
        ):
          self.feature_names = list(
              self.pipeline.steps[0][1].feature_names_in_
          )
        else:
          # Fallback matching your exact trained artifact naming scheme (Capitalized)
          self.feature_names = ["Amount"] + [f"V{i}" for i in range(1, 29)]

      self.is_loaded = True
      logger.info(
          f"Successfully loaded model from {model_path} with features:"
          f" {self.feature_names[:3]}..."
      )
    except Exception as e:
      logger.error(f"Failed to load model from {model_path}: {str(e)}")
      raise e

  def predict(self, amount: float, v_features: list) -> dict:
    if not self.is_loaded:
      raise RuntimeError("Model is not loaded.")

    input_data = [float(amount)] + [float(x) for x in v_features]

    # Create DataFrame with exact column names expected by the fitted pipeline
    df = pd.DataFrame([input_data], columns=self.feature_names)

    proba = float(self.pipeline.predict_proba(df)[0][1])
    is_fraud = bool(proba >= self.threshold)

    return {
        "is_fraud": is_fraud,
        "fraud_probability": round(proba, 4),
        "decision_threshold": self.threshold,
        "status": "FLAGGED" if is_fraud else "APPROVED",
    }


fraud_service = FraudService()