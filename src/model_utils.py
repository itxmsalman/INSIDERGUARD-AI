from pathlib import Path
from typing import Dict, List, Tuple

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

FEATURES: List[str] = [
    "after_hours_logins",
    "file_access_count",
    "email_activity",
    "device_activity",
    "web_activity",
]
TARGET = "insider_risk"


def project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def data_path() -> Path:
    return project_root() / "data" / "behavioural_demo.csv"


def model_path() -> Path:
    return project_root() / "models" / "insider_threat_model.joblib"


def load_data() -> pd.DataFrame:
    df = pd.read_csv(data_path())
    missing = [c for c in FEATURES + [TARGET] if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    return df


def train_model() -> Tuple[RandomForestClassifier, Dict[str, object]]:
    df = load_data()
    X = df[FEATURES]
    y = df[TARGET]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.30,
        random_state=42,
        stratify=y,
    )

    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42,
        class_weight="balanced",
    )
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    metrics = {
        "accuracy": float(accuracy_score(y_test, predictions)),
        "classification_report": classification_report(
            y_test, predictions, zero_division=0
        ),
        "confusion_matrix": confusion_matrix(y_test, predictions).tolist(),
        "train_rows": int(len(X_train)),
        "test_rows": int(len(X_test)),
        "dataset_rows": int(len(df)),
    }
    return model, metrics


def save_model(model: RandomForestClassifier) -> Path:
    path = model_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump({"model": model, "features": FEATURES}, path)
    return path


def load_model():
    path = model_path()
    if not path.exists():
        model, _ = train_model()
        save_model(model)
    bundle = joblib.load(path)
    return bundle["model"], bundle["features"]
