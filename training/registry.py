"""Model registry helpers for artifact versions and metadata."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODELS_DIR = PROJECT_ROOT / "models"
ARTIFACTS_DIR = MODELS_DIR / "artifacts"
METADATA_DIR = MODELS_DIR / "metadata"
REGISTRY_PATH = MODELS_DIR / "registry.json"


def ensure_registry_layout() -> None:
    """Create model registry directories and bootstrap registry.json."""
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    METADATA_DIR.mkdir(parents=True, exist_ok=True)
    if not REGISTRY_PATH.exists():
        save_registry({"current_version": None, "models": []})


def load_registry() -> dict:
    """Load the model registry from disk."""
    ensure_registry_layout()
    with REGISTRY_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_registry(registry: dict) -> None:
    """Persist the model registry to disk."""
    REGISTRY_PATH.parent.mkdir(parents=True, exist_ok=True)
    with REGISTRY_PATH.open("w", encoding="utf-8") as file:
        json.dump(registry, file, indent=2)


def get_next_model_version(registry: dict | None = None) -> str:
    """Generate the next model version label."""
    registry = registry or load_registry()
    next_version = len(registry["models"]) + 1
    return f"v{next_version}"


def build_artifact_path(version: str) -> Path:
    return ARTIFACTS_DIR / f"model_{version}.pkl"


def build_metadata_path(version: str) -> Path:
    return METADATA_DIR / f"model_{version}.json"


def register_model(version: str, metrics: dict[str, float], data_source: str, promote: bool = True) -> dict:
    """Record a model version in the registry and optionally promote it."""
    registry = load_registry()
    artifact_path = build_artifact_path(version)
    metadata_path = build_metadata_path(version)
    entry = {
        "version": version,
        "artifact_path": str(artifact_path),
        "metadata_path": str(metadata_path),
        "metrics": metrics,
        "data_source": data_source,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "is_production": promote,
    }
    registry["models"].append(entry)
    if promote:
        registry["current_version"] = version
    save_registry(registry)
    with metadata_path.open("w", encoding="utf-8") as file:
        json.dump(entry, file, indent=2)
    return entry


def promote_model(version: str) -> dict:
    """Promote an existing model entry to production."""
    registry = load_registry()
    promoted_entry = None
    for entry in registry["models"]:
        entry["is_production"] = entry["version"] == version
        metadata_path = Path(entry["metadata_path"])
        with metadata_path.open("w", encoding="utf-8") as file:
            json.dump(entry, file, indent=2)
        if entry["version"] == version:
            promoted_entry = entry
    registry["current_version"] = version
    save_registry(registry)
    if promoted_entry is None:
        raise ValueError(f"Unknown model version: {version}")
    return promoted_entry


def get_current_model_entry() -> dict | None:
    """Return the current production model entry, if any."""
    registry = load_registry()
    current_version = registry.get("current_version")
    if current_version is None:
        return None
    for entry in registry["models"]:
        if entry["version"] == current_version:
            return entry
    return None
