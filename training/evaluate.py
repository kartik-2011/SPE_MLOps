"""Evaluation utilities for regression metrics."""

from __future__ import annotations

from math import sqrt

from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


def calculate_regression_metrics(y_true, y_pred) -> dict[str, float]:
    """Return common regression metrics as floats."""
    mae = float(mean_absolute_error(y_true, y_pred))
    rmse = float(sqrt(mean_squared_error(y_true, y_pred)))
    r2 = float(r2_score(y_true, y_pred))
    return {
        "mae": mae,
        "rmse": rmse,
        "r2": r2,
    }
