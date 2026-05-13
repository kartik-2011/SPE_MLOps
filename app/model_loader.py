"""Utilities for loading the active production model."""

from __future__ import annotations

import joblib

from training.registry import get_current_model_entry


def load_current_model() -> tuple[object | None, dict | None]:
    """Load and return the current production model and registry entry."""
    entry = get_current_model_entry()
    if entry is None:
        return None, None
    model = joblib.load(entry["artifact_path"])
    return model, entry
