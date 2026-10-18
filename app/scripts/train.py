import joblib
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, roc_auc_score

def train_and_save_model(output_path: str = "artifacts/model_bundle.joblib"):
    print("Generating synthetic transaction dataset...")
    np.random.seed(42)
    n_samples = 10000
    
    v_features = np.random.randn(n_samples, 28)
    amount = np.random.exponential(scale=100, size=(n_samples, 1))
    X = np.hstack([amount, v_features])
    
    fraud_score = 0.05 * amount[:, 0] - 0.8 * X[:, 1] + 1.2 * X[:, 2] + np.random.randn(n_samples)
    y = (fraud_score > np.percentile(fraud_score, 99)).astype(int)
    
    feature_names = ["Amount"] + [f"V{i}" for i in range(1, 29)]
    df = pd.DataFrame(X, columns=feature_names)

    X_train, X_test, y_train, y_test = train_test_split(df, y, test_size=0.2, random_state=42, stratify=y)

    print("Training Logistic Regression Pipeline...")
    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('classifier', LogisticRegression(class_weight='balanced', max_iter=1000))
    ])
    
    pipeline.fit(X_train, y_train)

    y_pred_proba = pipeline.predict_proba(X_test)[:, 1]
    print(f"Model Trained. Test ROC-AUC Score: {roc_auc_score(y_test, y_pred_proba):.4f}")

    bundle = {
        "pipeline": pipeline,
        "feature_names": feature_names,
        "version": "1.0.0",
        "threshold": 0.85
    }
    
    joblib.dump(bundle, output_path)
    print(f"Model bundle successfully saved to {output_path}")

if __name__ == "__main__":
    train_and_save_model()