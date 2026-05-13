"""Baseline training entry point."""

from __future__ import annotations

import argparse
from pathlib import Path

import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

from training.data_loader import FEATURE_COLUMNS, TARGET_COLUMN, load_training_dataframe
from training.evaluate import calculate_regression_metrics
from training.registry import build_artifact_path, get_next_model_version, register_model


def train_model(
    data_source: str = "sklearn",
    csv_path: str | Path | None = None,
    random_state: int = 42,
    promote: bool = True,
) -> dict:
    """Train the baseline model, save it, and register the new version."""
    frame = load_training_dataframe(data_source=data_source, csv_path=csv_path)
    features = frame[FEATURE_COLUMNS]
    target = frame[TARGET_COLUMN]
    x_train, x_test, y_train, y_test = train_test_split(
        features,
        target,
        test_size=0.2,
        random_state=random_state,
    )

    model = RandomForestRegressor(
        n_estimators=200,
        random_state=random_state,
        n_jobs=-1,
    )
    model.fit(x_train, y_train)
    predictions = model.predict(x_test)
    metrics = calculate_regression_metrics(y_test, predictions)

    version = get_next_model_version()
    artifact_path = build_artifact_path(version)
    artifact_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, artifact_path)

    entry = register_model(version=version, metrics=metrics, data_source=data_source, promote=promote)
    entry["feature_columns"] = FEATURE_COLUMNS
    entry["target_column"] = TARGET_COLUMN
    entry["row_count"] = int(frame.shape[0])
    return entry


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train the baseline house price model.")
    parser.add_argument("--data-source", choices=["sklearn", "csv", "demo"], default="sklearn")
    parser.add_argument("--csv-path", default=None)
    parser.add_argument("--random-state", type=int, default=42)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    entry = train_model(
        data_source=args.data_source,
        csv_path=args.csv_path,
        random_state=args.random_state,
        promote=True,
    )
    print(f"Trained and registered model {entry['version']} with metrics {entry['metrics']}")


if __name__ == "__main__":
    main()
