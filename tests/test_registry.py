from training.registry import get_current_model_entry, load_registry


def test_registry_has_valid_shape():
    registry = load_registry()
    assert "current_version" in registry
    assert "models" in registry


def test_current_model_entry_is_optional():
    entry = get_current_model_entry()
    assert entry is None or "version" in entry
