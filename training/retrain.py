"""Retraining workflow for candidate models."""

from __future__ import annotations

import argparse
from pathlib import Path

from training.registry import get_current_model_entry, promote_model
from training.train import train_model


def should_promote(candidate_metrics: dict[str, float], current_metrics: dict[str, float] | None) -> bool:
    """Promote if there is no current model or candidate RMSE is lower."""
    if current_metrics is None:
        return True
    return candidate_metrics["rmse"] < current_metrics["rmse"]


def retrain_model(data_source: str = "sklearn", csv_path: str | Path | None = None) -> dict:
    """Train and compare a candidate model against the current production model."""
    current_entry = get_current_model_entry()
    current_metrics = current_entry["metrics"] if current_entry else None
    candidate_entry = train_model(data_source=data_source, csv_path=csv_path, promote=False)
    candidate_entry["promoted"] = should_promote(candidate_entry["metrics"], current_metrics)
    if candidate_entry["promoted"]:
        promoted_entry = promote_model(candidate_entry["version"])
        promoted_entry["promoted"] = True
        return promoted_entry
    return candidate_entry


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Retrain and evaluate a candidate model.")
    parser.add_argument("--data-source", choices=["sklearn", "csv", "demo"], default="sklearn")
    parser.add_argument("--csv-path", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    entry = retrain_model(data_source=args.data_source, csv_path=args.csv_path)
    print(f"Candidate model {entry['version']} metrics: {entry['metrics']}")
    print(f"Promoted: {entry['promoted']}")


if __name__ == "__main__":
    main()
