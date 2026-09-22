from __future__ import annotations

import json
import time
from pathlib import Path

import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline


ROOT = Path(__file__).resolve().parents[4]
DATASET_PATH = ROOT / "data" / "complaints_synthetic.csv"
ARTIFACT_DIR = Path(__file__).resolve().parent / "artifacts"
MODEL_PATH = ARTIFACT_DIR / "complaint_classifier.joblib"
METRICS_PATH = ARTIFACT_DIR / "metrics.json"


def load_dataset() -> pd.DataFrame:
    return pd.read_csv(DATASET_PATH)


def clean_dataset(data: pd.DataFrame) -> pd.DataFrame:
    cleaned = data.dropna(subset=["complaint", "department"]).copy()
    cleaned["complaint"] = cleaned["complaint"].astype(str).str.strip()
    cleaned["department"] = cleaned["department"].astype(str).str.strip()
    cleaned = cleaned[cleaned["complaint"] != ""]
    return cleaned


def build_pipeline() -> Pipeline:
    return Pipeline(
        steps=[
            ("tfidf", TfidfVectorizer(lowercase=True, ngram_range=(1, 2), min_df=2, max_features=30000)),
            ("classifier", LogisticRegression(max_iter=1000, class_weight="balanced", random_state=42)),
        ]
    )


def main() -> None:
    started = time.perf_counter()
    data = clean_dataset(load_dataset())
    x_train, x_test, y_train, y_test = train_test_split(
        data["complaint"],
        data["department"],
        test_size=0.2,
        random_state=42,
        stratify=data["department"],
    )
    pipeline = build_pipeline()
    pipeline.fit(x_train, y_train)
    predictions = pipeline.predict(x_test)
    accuracy = accuracy_score(y_test, predictions)
    precision, recall, f1, _ = precision_recall_fscore_support(
        y_test,
        predictions,
        average="macro",
        zero_division=0,
    )
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipeline, MODEL_PATH)
    elapsed = time.perf_counter() - started
    metrics = {
        "data_source": "SYNTHETIC TRAINING DATA",
        "records": int(len(data)),
        "train_records": int(len(x_train)),
        "test_records": int(len(x_test)),
        "accuracy": round(float(accuracy), 6),
        "macro_precision": round(float(precision), 6),
        "macro_recall": round(float(recall), 6),
        "macro_f1": round(float(f1), 6),
        "training_seconds": round(elapsed, 4),
    }
    METRICS_PATH.write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    print(json.dumps(metrics, indent=2))
    print(f"model={MODEL_PATH}")


if __name__ == "__main__":
    main()
