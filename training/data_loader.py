"""Dataset loading utilities for baseline and future CSV-based training."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.datasets import fetch_california_housing

TARGET_COLUMN = "MedHouseVal"
FEATURE_COLUMNS = [
    "MedInc",
    "HouseAge",
    "AveRooms",
    "AveBedrms",
    "Population",
    "AveOccup",
    "Latitude",
    "Longitude",
]
PROJECT_ROOT = Path(__file__).resolve().parents[1]
SKLEARN_DATA_HOME = PROJECT_ROOT / "data" / "raw" / "sklearn"


def load_california_housing_dataset() -> pd.DataFrame:
    """Return the built-in California housing dataset as a DataFrame."""
    SKLEARN_DATA_HOME.mkdir(parents=True, exist_ok=True)
    try:
        dataset = fetch_california_housing(as_frame=True, data_home=str(SKLEARN_DATA_HOME))
        frame = dataset.frame.copy()
        ordered_columns = FEATURE_COLUMNS + [TARGET_COLUMN]
        return frame[ordered_columns]
    except Exception:
        return load_demo_housing_dataset()


def load_demo_housing_dataset(rows: int = 1000, random_state: int = 42) -> pd.DataFrame:
    """Generate a deterministic demo dataset when external data is unavailable."""
    rng = np.random.default_rng(random_state)
    frame = pd.DataFrame(
        {
            "MedInc": rng.uniform(1.5, 15.0, rows),
            "HouseAge": rng.integers(1, 52, rows),
            "AveRooms": rng.uniform(3.0, 9.5, rows),
            "AveBedrms": rng.uniform(0.8, 2.5, rows),
            "Population": rng.integers(300, 6000, rows),
            "AveOccup": rng.uniform(1.5, 6.0, rows),
            "Latitude": rng.uniform(32.0, 42.0, rows),
            "Longitude": rng.uniform(-124.0, -114.0, rows),
        }
    )
    noise = rng.normal(0, 0.25, rows)
    frame[TARGET_COLUMN] = (
        0.45 * frame["MedInc"]
        + 0.018 * frame["HouseAge"]
        + 0.12 * frame["AveRooms"]
        - 0.28 * frame["AveBedrms"]
        - 0.00007 * frame["Population"]
        - 0.06 * frame["AveOccup"]
        + 0.015 * (42.0 - frame["Latitude"])
        + 0.02 * (-114.0 - frame["Longitude"])
        + noise
    ).clip(lower=0.5)
    return frame[FEATURE_COLUMNS + [TARGET_COLUMN]]


def load_csv_dataset(csv_path: str | Path) -> pd.DataFrame:
    """Load a CSV dataset that contains the expected feature set."""
    frame = pd.read_csv(csv_path)
    missing_columns = [column for column in FEATURE_COLUMNS + [TARGET_COLUMN] if column not in frame.columns]
    if missing_columns:
        missing_text = ", ".join(missing_columns)
        raise ValueError(f"CSV dataset is missing required columns: {missing_text}")
    return frame[FEATURE_COLUMNS + [TARGET_COLUMN]]


def load_training_dataframe(data_source: str = "sklearn", csv_path: str | Path | None = None) -> pd.DataFrame:
    """Load training data from either sklearn or a local CSV file."""
    if data_source == "sklearn":
        return load_california_housing_dataset()
    if data_source == "demo":
        return load_demo_housing_dataset()
    if data_source == "csv":
        if csv_path is None:
            raise ValueError("csv_path is required when data_source='csv'")
        return load_csv_dataset(csv_path)
    raise ValueError(f"Unsupported data source: {data_source}")
