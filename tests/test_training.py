from training.train import train_model


def test_train_model_registers_new_version():
    entry = train_model(data_source="demo")
    assert entry["version"].startswith("v")
    assert entry["metrics"]["rmse"] > 0
    assert entry["row_count"] > 0
