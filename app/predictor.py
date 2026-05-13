"""Prediction helpers for the inference API."""

from __future__ import annotations

import pandas as pd

from training.data_loader import FEATURE_COLUMNS

from app.schema import PredictionRequest


def predict_price(model, payload: PredictionRequest) -> float:
    """Generate a single house price prediction."""
    feature_frame = pd.DataFrame([payload.to_feature_list()], columns=FEATURE_COLUMNS)
    prediction = model.predict(feature_frame)
    return float(prediction[0])
