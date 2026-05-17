"""Utilities for loading the active production model."""

from __future__ import annotations

from pathlib import Path

import joblib

from training.registry import PROJECT_ROOT, get_current_model_entry, normalize_registry_paths


def resolve_project_path(path_value: str) -> Path:
    """Resolve a registry path against the current project root if needed."""
    candidate = Path(path_value)
    if candidate.is_absolute() and candidate.exists():
        return candidate
    parts = candidate.parts
    if "models" in parts:
        models_index = parts.index("models")
        fallback = PROJECT_ROOT.joinpath(*parts[models_index:])
        if fallback.exists():
            return fallback
    if candidate.is_absolute():
        try:
            relative_candidate = candidate.relative_to(candidate.anchor)
            fallback = PROJECT_ROOT / relative_candidate
            if fallback.exists():
                return fallback
        except ValueError:
            pass
    fallback = PROJECT_ROOT / candidate
    return fallback


def load_current_model() -> tuple[object | None, dict | None]:
    """Load and return the current production model and registry entry."""
    normalize_registry_paths()
    entry = get_current_model_entry()
    if entry is None:
        return None, None
    artifact_path = resolve_project_path(entry["artifact_path"])
    model = joblib.load(artifact_path)
    return model, entry
