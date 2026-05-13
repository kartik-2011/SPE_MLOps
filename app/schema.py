"""Pydantic schemas for request and response models."""

from __future__ import annotations

from pydantic import BaseModel


class PredictionRequest(BaseModel):
    MedInc: float
    HouseAge: float
    AveRooms: float
    AveBedrms: float
    Population: float
    AveOccup: float
    Latitude: float
    Longitude: float

    def to_feature_list(self) -> list[float]:
        return [
            self.MedInc,
            self.HouseAge,
            self.AveRooms,
            self.AveBedrms,
            self.Population,
            self.AveOccup,
            self.Latitude,
            self.Longitude,
        ]


class PredictionResponse(BaseModel):
    prediction: float
    model_version: str


class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
    model_version: str | None = None


class ModelInfoResponse(BaseModel):
    current_version: str | None
    metrics: dict[str, float] | None
    data_source: str | None
